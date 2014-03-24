"""
Tests for the Article Extractor artex.

"""
import os
import unittest

from django.test import TestCase
from django.conf import settings

from artex import Article


class ArticleTest(TestCase):
    """Tests for the article extraction from an HTML page. """
    def setUp(self):
        self.fixtures_dir = os.path.join(settings.PROJECT_ROOT,
                                         'artex/fixtures/')

    def test_Artex_djangoblog(self):
        html_file = os.path.join(self.fixtures_dir, 'django-blogpost.html')
        html = open(html_file, 'r').read()
        article = Article(html)
        # print(article.title)
        self.assertEqual(article.title, 'Security advisory: strip_tags safety')
