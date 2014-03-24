# -*- coding: utf-8 -*-
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
        self.assertEqual(article.title, 'Security advisory: strip_tags safety')
        self.assertEqual(article.content[:20], '<p>We\'ve received a ')
        self.assertEqual(article.content[-10:], ', 2014</p>')

    def test_Artex_wordpress(self):
        html_file = os.path.join(self.fixtures_dir, 'wordpress-blogpost.html')
        html = open(html_file, 'r').read()
        article = Article(html)
        self.assertEqual(article.title, u'WordPress 3.8 “Parker”')
        self.assertEqual(article.content[:20], '<p>Version 3.8 of Wo')
        self.assertEqual(article.content[-20:], 'for version 3.9!</p>')
