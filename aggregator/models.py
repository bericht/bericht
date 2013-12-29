import os
import logging
from time import mktime
from datetime import datetime

import requests
import feedparser
from taggit.managers import TaggableManager

from readability.readability import Document

from django.conf import settings
from django.db import models
from django.dispatch import Signal, receiver
from django.utils.timezone import get_current_timezone, make_aware, now
from django.template.defaultfilters import slugify

logger = logging.getLogger(__name__)

fetched_feed_file = Signal()


class FeedFile(models.Model):
    """The class that fetches the feed file

    This class fetches the feed file and stores the feed file contents. It also
    takes care to minimize used bandwidth and supports archiving the feed files
    to the local storage.
    """
    #: The url from where the feed file is to be fetched. Has to be unique.
    url = models.URLField(unique=True)
    #: The contents of the feed file.
    body = models.TextField()
    #: When this feed file has been updated the last time. Defaults to now.
    updated_at = models.DateTimeField(auto_now=True)
    #: The ETag is a special header that some feed publishers support to reduce
    #: bandwidth.
    etag = models.CharField(max_length=128, blank=True)
    #: The last modified header is also supported by some publishers to reduce
    #: bandwidth.
    modified = models.CharField(max_length=40, blank=True)

    def __unicode__(self):
        return self.url

    def fetch(self):
        """Fetches the feed file in a bandwidth-friendly way

        Tries to only fetch the new items if the feed publisher supports ETag
        and/or last_modified HTTP headers. It also archives the fetched
        file and parses the file by using the model Feed.
        """
        logger.info("fetching feed at '%s'..." % self.url)
        try:
            headers = {'user-agent': feedparser.USER_AGENT,
                       'If-None-Match': self.etag,
                       'If-Modified-Since': self.modified}
            req = requests.get(self.url, headers=headers, verify=False)
        except Exception as e:
            logger.error(e)
            return None

        """
        If the HTTP status code is 304, the feed didn't change since the last
        time the file was fetched, thus no further processing useful.
        """
        if req.status_code == 304:
            self.save()
            return True

        if req.status_code != 200:
            raise requests.HTTPError("error while fetching '%s': %s" %
                                     (self.url, req.status_code))
        self.body = req.content
        self.etag = req.headers.get('etag', '')
        self.modified = req.headers.get('last-modified', '')
        self.save()
        self.archive(self.url, self.body)
        fetched_feed_file.send(sender=self)
        return True

    def archive(self, url, content):
        timestamp = datetime.now().strftime('%Y-%m-%d-%H-%M-%S.rss')
        directory = os.path.join(settings.ARCHIVE_DIR, slugify(url))
        filename = os.path.join(directory, timestamp)
        if not os.path.isdir(directory):
            os.makedirs(directory)
        with open(filename, "w") as f:
            f.write(content)

    @classmethod
    def fetch_all(cls):
        for feed_file in cls.objects.all():
            feed_file.fetch()

parsed_item = Signal(providing_args=['entry'])


class Feed(models.Model):
    feed_file = models.OneToOneField(FeedFile)

    title = models.CharField(max_length=512, default=None)
    link = models.URLField(default=None)
    description = models.TextField(default=None)
    updated_at = models.DateTimeField()
    parsed_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.title

    @classmethod
    def from_file(cls, feed_file):
        parsed = feedparser.parse(feed_file.body)
        feed, new = cls.objects.get_or_create(
            feed_file=feed_file,
            defaults={
                'title': parsed.feed.get('title', None),
                'link': parsed.feed.get('link', None),
                # @TODO: sanitize html (XSS,..)
                'description': parsed.feed.get('description', None),
                'updated_at': now()
            })
        feed.save()

        status = "new" if new else "updated"
        logger.info("parsed %s feed: %s" % (status, feed.feed_file.url))

        for entry in parsed.entries:
            parsed_item.send(sender=feed, entry=entry)

        return feed


@receiver(fetched_feed_file)
def parse_feed_file(sender, **kwargs):
    Feed.from_file(sender)


class Item(models.Model):
    feed = models.ForeignKey(Feed)

    title = models.CharField(max_length=512)
    link = models.URLField()
    tags = TaggableManager()
    description = models.TextField()
    #: Holds the datetime when this item was published or updated.
    updated_at = models.DateTimeField()
    #: If the feed comes with the full content (not only the summary), populate
    #: this.
    content = models.TextField(blank=True)
    #: Stores the way content was obtained:
    content_source = models.CharField(max_length=32)
    #: This holds the HTML of the item link at the time it got parsed.
    link_html = models.TextField(blank=True)

    def __unicode__(self):
        return "[%s] %s" % (self.feed.title, self.title)

    def slug(self):
        return "%s-%s" % (slugify(self.feed.title),
                          slugify(self.title))

    @classmethod
    def from_feed_entry(cls, feed, entry):
        if 'updated' in entry:
            updated_at = parse_time(entry.updated_parsed)
        else:
            updated_at = parse_time(entry.published_parsed)
        item, new = cls.objects.get_or_create(
            feed=feed, link=entry.link, title=entry.title,
            defaults={
                # @TODO: sanitize html (XSS,..)
                'description': entry.description,
                'updated_at': updated_at,
            })

        if 'tags' in entry and 'term' in entry.tags[0]:
            item.tags.add(*[tag.term for tag in entry.tags])

        # try to get the entry content in suitable format if supplied
        # see http://pythonhosted.org/feedparser/reference-entry-content.html
        if 'content' in entry:
            for c in entry.content:
                if c.type in ['text/plain', 'text/html',
                              'application/xhtml+xml']:
                    item.content = c.value
                    item.content_source = 'feed'
                    # for now take the first suitable content and exit the loop
                    break

        # fetching and storing the HTML of the linked web page
        # @TODO only if content is empty or always for archiving?
        req = requests.get(item.link, headers={'user-agent': 'readability'},
                           verify=False)
        if req.status_code != 200:
            raise requests.HTTPError("error while fetching HTML of '%s': %s" %
                                     (item.link, req.status_code))
        item.link_html = req.content
        # extract article from html if content is empty:
        if item.content == '':
            item.content = Document(req.content).summary(html_partial=True)
            item.content_source = 'original page'
        item.save()

        status = "new" if new else "updated"
        logger.info("parsed %s item: %s" % (status, feed.feed_file.url))


@receiver(parsed_item)
def save_item(sender, **kwargs):
    Item.from_feed_entry(sender, kwargs['entry'])


# @TODO: Should probably be somewhere elsse ;)
def parse_time(time_struct):
    return make_aware(datetime.fromtimestamp(mktime(time_struct)),
                      get_current_timezone())
