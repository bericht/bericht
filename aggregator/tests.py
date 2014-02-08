"""
Tests for the aggregator

"""
import os
import datetime
from libpathod import test

from django.test import TestCase
from django.conf import settings

from aggregator.models import FeedFile, Feed


class FeedFileTest(TestCase):
    """ Tests the fetching process of a given feed.
    uses pathod.net to emulate a broken http server.

    """
    def setUp(self):
        fixtures_dir = os.path.join(settings.PROJECT_ROOT,
                                    'aggregator/fixtures/')
        self.d = test.Daemon(staticdir=fixtures_dir)
        self.valid_feed = os.path.join(fixtures_dir, 'django.rss')

    def tearDown(self):
        self.d.shutdown()

    def test_200_reponse(self):
        """ Does it work if get a okay response? """
        url = self.d.p('200:b<"%s"' % self.valid_feed)
        feed_file = FeedFile(url=url)

        with self.assertRaises(Feed.DoesNotExist):
            Feed.objects.get(feed_file=feed_file)
        feed_file.fetch()
        feed = Feed.objects.get(feed_file=feed_file)

        self.assertEqual(feed.title, 'The Django weblog')
        self.assertEqual(feed.link, 'https://www.djangoproject.com/weblog/')
        self.assertEqual(feed.description, '<div>Latest news about Django, ' +
                         'the Python Web framework.</div>')
        self.assertIsInstance(feed.updated_at, datetime.datetime)
        self.assertIsInstance(feed.parsed_at, datetime.datetime)
