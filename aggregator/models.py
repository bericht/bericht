import os
import logging
from time import mktime
from datetime import datetime

import requests
import feedparser
from taggit.managers import TaggableManager
from lxml.html.clean import clean_html
from lxml.html.soupparser import fromstring
from lxml.etree import tostring

from django.conf import settings
from django.db import models
from django.dispatch import Signal, receiver
from django.utils.timezone import get_current_timezone, make_aware, now
from django.template.defaultfilters import slugify

from article.models import ImportedArticle

logger = logging.getLogger(__name__)

fetched_feed_file = Signal()
parsed_item = Signal(providing_args=['entry'])
saved_feeditem = Signal()


@receiver(fetched_feed_file)
def parse_feed_file(sender, **kwargs):
    Feed.from_file(sender)


@receiver(parsed_item)
def save_item(sender, **kwargs):
    FeedItem.from_feed_entry(sender, kwargs['entry'])


@receiver(saved_feeditem)
def create_article(sender, **kwargs):
    ImportedArticle.from_feeditem(sender)


# @TODO Uses a blacklist by default, we might want to replace that with a
# whitelist.
def sanitize(html):
    return tostring(clean_html(fromstring(html)))


def parse_time(time_struct):
    return make_aware(datetime.fromtimestamp(mktime(time_struct)),
                      get_current_timezone())


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
            headers = {'user-agent': feedparser.USER_AGENT, }
            # only set headers if they were set:
            if self.etag != '':
                headers['If-None-Match'] = self.etag
            if self.modified != '':
                headers['If-Modified-Since'] = self.modified

            req = requests.get(self.url, headers=headers, verify=False)
        except Exception as e:
            logger.error(e)
            return None

        # If the HTTP status code is 304, the feed didn't change since the last
        # time the file was fetched, thus no further processing useful.
        if req.status_code == 304:
            self.save()
            return True

        if req.status_code != 200:
            logger.error("error while fetching '%s': %s" %
                         (self.url, req.status_code))
            return

        self.body = req.content
        self.etag = req.headers.get('etag', '')
        self.modified = req.headers.get('last-modified', '')
        self.save()
        self.archive(self.url, self.body)
        fetched_feed_file.send(sender=self)

        return self

    def archive(self, url, content, timestamp=datetime.now()):
        filename = timestamp.strftime('%Y-%m-%d-%H-%M-%S.rss')
        directory = os.path.join(settings.ARCHIVE_DIR, slugify(url))
        filepath = os.path.join(directory, filename)
        if not os.path.isdir(directory):
            os.makedirs(directory)
        with open(filepath, "w") as f:
            f.write(content)

    @classmethod
    def fetch_all(cls):
        for feed_file in cls.objects.all():
            feed_file.fetch()


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
                'title': parsed.feed.get('title', feed_file.url),
                'link': parsed.feed.get('link', None),
                'description': sanitize(parsed.feed.get('description', '')),
                'updated_at': now()
            })
        feed.save()

        status = "new" if new else "updated"
        logger.info("parsed %s feed: %s" % (status, feed.feed_file.url))

        for entry in parsed.entries:
            parsed_item.send(sender=feed, entry=entry)

        return feed


class FeedItem(models.Model):
    #: The Feed this FeedItem belongs to.
    feed = models.ForeignKey(Feed)

    #: The title of the FeedItem.
    title = models.CharField(max_length=512)
    #: The url this FeedItem points to, courtesy of the link attribute.
    link = models.URLField()
    #: Tags that are provided in the FeedItem.
    tags = TaggableManager()
    #: Description is usually the teaser/summary, i.e. a shorter content.
    description = models.TextField()
    #: Holds the datetime when this item was published or updated.
    updated_at = models.DateTimeField()
    #: If the feed comes with the full content (not only the summary), populate
    #: this.
    content = models.TextField(blank=True)
    #: This holds the HTML of the item link at the time it got parsed.
    link_html = models.TextField(blank=True)

    def __unicode__(self):
        return "[%s] %s" % (self.feed.title, self.title)

    def slug(self):
        return "%s-%s" % (slugify(self.feed.title),
                          slugify(self.title))

    def get_content(self):
        return self.content or self.description

    @classmethod
    def from_feed_entry(cls, feed, entry):
        item, new = cls.objects.get_or_create(
            feed=feed, link=entry.link, title=entry.title,
            defaults={
                'description': sanitize(entry.description),
                'updated_at': cls._get_date_of_update(entry),
            })
        item.tags.add(*cls._get_tags(entry))
        item.content = cls._get_item_content_as_text(entry)
        item.save()

        status = "new" if new else "updated"
        logger.info("parsed %s item: %s [from %s]" % (status, feed.link,
                                                      feed.feed_file.url))
        saved_feeditem.send(sender=item)

    @classmethod
    def _get_date_of_update(cls, entry):
        if 'updated' in entry:
            return parse_time(entry.updated_parsed)
        else:
            return parse_time(entry.published_parsed)

    @classmethod
    def _get_item_content_as_text(cls, entry):
        # try to get the entry content in suitable format if supplied
        # see http://pythonhosted.org/feedparser/reference-entry-content.html
        if 'content' in entry:
            for c in entry.content:
                if c.type in ['text/plain', 'text/html',
                              'application/xhtml+xml']:
                    # @TODO sanitize
                    return c.value
        return ''  # if we did not return something else so far

    @classmethod
    def _get_tags(cls, entry):
        if 'tags' in entry and 'term' in entry.tags[0]:
            return [tag.term for tag in entry.tags]
        else:
            return []
