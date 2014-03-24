# -*- coding: utf-8 -*-
"""
Tests for the Article Extractor artex.

"""
import os
import unittest

from django.test import TestCase
from django.conf import settings
from lxml import etree
from artex import Article
import artex


class ArticleTest(TestCase):
    """Tests for the article extraction from an HTML page. """
    def setUp(self):
        self.fixtures_dir = os.path.join(settings.PROJECT_ROOT,
                                         'artex/fixtures/')

    def test_Artex_djangoblog(self):
        """Tests correct article extraction on a Djangoproject Blog post."""
        html_file = os.path.join(self.fixtures_dir, 'django-blogpost.html')
        html = open(html_file, 'r').read()
        article = Article(html)
        self.assertEqual(article.title, 'Security advisory: strip_tags safety')
        self.assertEqual(article.content[:20], '<p>We\'ve received a ')
        self.assertEqual(article.content[-10:], ', 2014</p>')

    def test_Artex_wordpress(self):
        """Tests correct article extraction on a WordPress.org blog post."""
        html_file = os.path.join(self.fixtures_dir, 'wordpress-blogpost.html')
        html = open(html_file, 'r').read()
        article = Article(html)
        self.assertEqual(article.title, u'WordPress 3.8 “Parker”')
        self.assertEqual(article.content[:20], '<p>Version 3.8 of Wo')
        self.assertEqual(article.content[-20:], 'for version 3.9!</p>')

    def test_contains_text_before_p(self):
        """Tests that text in the outer div before a p is retained."""
        html = '<div>this is valuable text<p>and here is more</p></div>'
        self.assertTrue(artex.contains_text(etree.fromstring(html)))

    def test_contains_text_between_p(self):
        """Tests that text in the outer div before a p is retained."""
        html = '''
        <div><p>This is text. </p>This is valuable text<p>and
        here is more</p></div>
        '''
        self.assertTrue(artex.contains_text(etree.fromstring(html)))

    def test_contains_text_after_p(self):
        """Tests that text in the outer div before a p is retained."""
        html = '<div><p>This is text. </p>This is valuable text.</div>'
        self.assertTrue(artex.contains_text(etree.fromstring(html)))

    def test_cleanup_and_text_between_children(self):
        """
        Tests that cleanup maintains text between children of enclosing
        div.
        """
        html = '<div>text <p>text </p>text <p>text </p>text</div>'
        target = 'text <p>text </p>text <p>text </p>text'
        self.assertEqual(artex.cleanup(etree.fromstring(html)), target)
