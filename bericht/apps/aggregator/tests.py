"""
Tests for the aggregator

"""
import os
import datetime
import httpretty

from django.test import TestCase
from django.conf import settings
from django.template.defaultfilters import slugify

from .models import FeedFile, Feed, FeedItem


class FeedFileTest(TestCase):
    """ Tests the fetching process of a given feed.
    uses pathod.net to emulate a broken http server.

    """
    def setUp(self):
        httpretty.enable()
        fixtures_dir = os.path.join(settings.PROJECT_ROOT,
                                    'apps/aggregator/fixtures/')
        feed_path = os.path.join(fixtures_dir, 'django.rss')
        with open(feed_path, 'r') as f:
            self.valid_feed = f.read()

    def mock_url(self, path, status, body, headers={}):
        url = "http://testing/%s" % path
        httpretty.register_uri(
            httpretty.GET, url,
            status=status, body=body, adding_headers=headers)
        return url

    def test_200_reponse(self):
        """ Does it work if get a okay response? """
        url = self.mock_url('200', '200', self.valid_feed)
        feed_file = FeedFile(url=url)

        with self.assertRaises(Feed.DoesNotExist):
            Feed.objects.get(feed_file=feed_file)
        feed_file.fetch()

    def test_304_response(self):
        """ If response status is 304, only FeedFile.updated_at should
        change. """
        url = self.mock_url('304', '304', '')
        feed_file = FeedFile(url=url)
        feed_file.fetch()
        # if status is 304, fetch return before sending file content to Feed:
        with self.assertRaises(Feed.DoesNotExist):
            Feed.objects.get(feed_file=feed_file)

    def test_etag_if_present(self):
        """ Test that etag is stored correctly if set by server. """
        # set the Etag header and supply working feed.
        etag = 'test_etag_if_present'
        url = self.mock_url('etag', '200', self.valid_feed, {'Etag': etag})
        feed_file = FeedFile(url=url)
        feed_file.fetch()
        # check if the etag was saved at the FeedFile
        self.assertEqual(feed_file.etag, etag)
        # check that If-None-Match header is set at next request
        # feed_file.fetch()
        # headers = self.d.log()[:1][0]['request']['headers']
        # self.assertEqual(filter(lambda a: a[0] == 'If-None-Match',
        #                        headers)[0][1], etag)

    def test_last_modified_if_present(self):
        """ Test that last-modified is set correctly if provided
        by response."""
        # set the last-modified header and supply working feed.
        last_modified = 'test_last-modified_if_present'
        url = self.mock_url('modified', '200', self.valid_feed,
                            {'Last-Modified': last_modified})
        feed_file = FeedFile(url=url)
        feed_file.fetch()
        # check if the Last-Modified was saved at the FeedFile
        self.assertEqual(feed_file.modified, last_modified)
        # check that If-None-Match header is set at next request
        # feed_file.fetch()
        # headers = self.d.log()[:1][0]['request']['headers']
        # self.assertEqual(filter(lambda a: a[0] == 'If-Modified-Since',
        #                         headers)[0][1], last_modified)

    def test_headers_if_absent(self):
        """ Test that empty string is stored if last-modified header is
        not provided. """
        # set the last-modified header and supply working feed.
        url = self.mock_url('200', '200', self.valid_feed)
        feed_file = FeedFile(url=url)
        feed_file.fetch()
        self.assertEqual(feed_file.modified, '')
        # check that If-None-Match header is set at next request
        # feed_file.fetch()
        # headers = self.d.log()[:1][0]['request']['headers']
        # self.assertFalse([u'If-None-Match', u''] in headers)
        # self.assertFalse([u'If-Modified-Since', u''] in headers)

    def test_archiving(self):
        """ Test that the archive is stored correctly. """
        url = self.mock_url('200', '200', self.valid_feed)
        feed_file = FeedFile(url=url)
        feed_file.fetch()
        # call FeedFile.archive(..) with manually set timestamp
        timestamp = datetime.datetime.now()
        feed_file.archive(feed_file.url, feed_file.body, timestamp)
        # verify that the file exists
        filepath = os.path.join(os.path.join(settings.ARCHIVE_DIR,
                                             slugify(feed_file.url)),
                                timestamp.strftime('%Y-%m-%d-%H-%M-%S.rss'))
        archived_feed = open(filepath, "r").read()
        # verify that the file content is the same as the source file
        self.assertEqual(self.valid_feed, archived_feed)

    def test_404_response(self):
        pass

    def test_500_response(self):
        pass

    def test_302_response(self):
        pass


class FeedTest(TestCase):
    """ Tests the parsing of a FeedFile into the Feed model. """

    def setUp(self):
        httpretty.enable()
        fixtures_dir = os.path.join(settings.PROJECT_ROOT,
                                    'apps/aggregator/fixtures/')
        url = 'http://testing/feed'
        with open(os.path.join(fixtures_dir, 'django.rss'), 'r') as f:
            body = f.read()
        httpretty.register_uri(httpretty.GET, url, body=body)
        self.feed_file = FeedFile(url=url)

    def test_parsing(self):
        """ Tests that feed title, link, description are correct and that
        dates are parsed correctly. """
        self.feed_file.fetch()
        feed = Feed.objects.get(feed_file=self.feed_file)

        self.assertEqual(feed.title, 'The Django weblog')
        self.assertEqual(feed.link, 'https://www.djangoproject.com/weblog/')
        self.assertEqual(feed.description, '<p>Latest news about Django, ' +
                         'the Python Web framework.</p>')
        self.assertIsInstance(feed.updated_at, datetime.datetime)
        self.assertIsInstance(feed.parsed_at, datetime.datetime)

    def test_number_items(self):
        """ Tests that the feed parses all items, i.e. checks that the
        number of items equals the number of entries of the feed file. """
        self.feed_file.fetch()
        feed = Feed.objects.get(feed_file=self.feed_file)
        items = FeedItem.objects.filter(feed=feed)
        self.assertEqual(len(items), 10)
