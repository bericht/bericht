import os
import logging
from time import mktime
from datetime import datetime

import requests
import feedparser

from django.conf import settings
from django.db import models
from django.dispatch import Signal, receiver
from django.utils.timezone import get_current_timezone, make_aware, now
from django.template.defaultfilters import slugify

logger = logging.getLogger(__name__)

fetched_feed_file = Signal()


class FeedFile(models.Model):
    url = models.URLField(unique=True)
    body = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.url

    def fetch(self):
        logger.info("fetching feed at '%s'..." % self.url)
        try:
            headers = {'user-agent': feedparser.USER_AGENT}
            req = requests.get(self.url, headers=headers, verify=False)
        except Exception as e:
            logger.error(e)
            return None

        if req.status_code != 200:
            raise requests.HTTPError("error while fetching '%s': %s" %
                                     (self.url, req.status_code))
        self.body = req.content
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
    description = models.TextField()
    updated_at = models.DateTimeField()

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
            feed=feed, link=entry.link,
            defaults={
                'title': entry.title,
                # @TODO: sanitize html (XSS,..)
                'description': entry.description,
                'updated_at': updated_at,
            })
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
