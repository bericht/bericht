"""
Tests for the aggregator

"""
import os
import datetime
from libpathod import test

from django.test import TestCase
from django.conf import settings
from django.template.defaultfilters import slugify

from aggregator.models import FeedItem, FeedFile
from article.models import ImportedArticle


class ImportedArticleTest(TestCase):
    """ Tests the creation of ImportedArticle from FeedItems """

    def setUp(self):
        fixtures_dir = os.path.join(settings.PROJECT_ROOT,
                                    'aggregator/fixtures/')
        self.d = test.Daemon(staticdir=fixtures_dir)
        self.valid_feed = os.path.join(fixtures_dir, 'django.rss')
        url = self.d.p('200:b<"%s"' % self.valid_feed)
        self.feed_file = FeedFile(url=url)
        self.feed_file.fetch()

    def tearDown(self):
        self.d.shutdown()

    def test_importedarticle_creation(self):
        num_feeditems = len(FeedItem.objects.all())
        num_importedarticles = len(ImportedArticle.objects.all())
        self.assertEqual(num_feeditems, num_importedarticles)
        feeditem = FeedItem.objects.first()
        importedarticle = ImportedArticle.objects.get(title=feeditem.title)
        self.assertEqual(feeditem.description, importedarticle.teaser)
        self.assertEqual(feeditem.updated_at, importedarticle.created_at)
        for tag in feeditem.tags.all():
            self.assertTrue(tag in importedarticle.tags.all())
