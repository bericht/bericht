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

    def test_304_response(self):
        """ If response status is 304, only FeedFile.updated_at should
        change. """
        url = self.d.p('304')
        feed_file = FeedFile(url=url)
        feed_file.fetch()
        # if status is 304, fetch return before sending file content to Feed:
        with self.assertRaises(Feed.DoesNotExist):
            Feed.objects.get(feed_file=feed_file)

    def test_etag_if_present(self):
        """ Test that etag is stored correctly if set by server. """
        pass

    def test_last_modified_if_present(self):
        """ Test that last-modified is set correctly if provided
        by response."""
        pass

    def test_etag_if_absent(self):
        """ Test that empty string is stored if etag is not provided. """
        pass

    def test_last_modified_if_absent(self):
        """ Test that empty string is stored if last-modified header is
        not provided. """
        pass

    def test_archiving(self):
        """ Test that the archive is stored correctly. """
        # TODO call FeedFile.archive(..) with manually set timestamp
        # TODO verify that the file exists
        # TODO verify that the file content is the same as the source file
        pass


class FeedTest(TestCase):
    """ Tests the parsing of a FeedFile into the Feed model. """

    def setUp(self):
        fixtures_dir = os.path.join(settings.PROJECT_ROOT,
                                    'aggregator/fixtures/')
        self.d = test.Daemon(staticdir=fixtures_dir)
        self.valid_feed = os.path.join(fixtures_dir, 'django.rss')
        url = self.d.p('200:b<"%s"' % self.valid_feed)
        self.feed_file = FeedFile(url=url)

    def tearDown(self):
        self.d.shutdown()

    def test_parsing(self):
        """ Tests that feed title, link, description are correct and that
        dates are parsed correctly. """
        self.feed_file.fetch()
        feed = Feed.objects.get(feed_file=self.feed_file)

        self.assertEqual(feed.title, 'The Django weblog')
        self.assertEqual(feed.link, 'https://www.djangoproject.com/weblog/')
        self.assertEqual(feed.description, '<div>Latest news about Django, ' +
                         'the Python Web framework.</div>')
        self.assertIsInstance(feed.updated_at, datetime.datetime)
        self.assertIsInstance(feed.parsed_at, datetime.datetime)
