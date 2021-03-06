# -*- coding: utf-8 -*-
"""
Tests for the Article Extractor artex.

"""
import os
import unittest

from django.test import TestCase
from django.conf import settings
from lxml import etree
from bericht.apps.artex import (contains_text, cleanup, elem_content_to_string,
                                extract_article)


class ArticleTest(TestCase):
    """Tests for the article extraction from an HTML page. """
    def setUp(self):
        self.fixtures_dir = os.path.join(settings.PROJECT_ROOT,
                                         'apps/artex/fixtures/')

    def test_Artex_djangoblog(self):
        """Tests correct article extraction on a Djangoproject Blog post."""
        html_file = os.path.join(self.fixtures_dir, 'django-blogpost.html')
        html = open(html_file, 'r').read()
        title, content = extract_article(html)
        self.assertEqual(title, 'Security advisory: strip_tags safety')
        self.assertEqual(content[:20], '<p>We\'ve received a ')
        self.assertEqual(content[-10:], ', 2014</p>')

    def test_Artex_wordpress(self):
        """Tests correct article extraction on a WordPress.org blog post."""
        html_file = os.path.join(self.fixtures_dir, 'wordpress-blogpost.html')
        html = open(html_file, 'r').read()
        title, content = extract_article(html)
        self.assertEqual(title, u'WordPress 3.8 “Parker”')
        self.assertEqual(content[:20], '<p>Version 3.8 of Wo')
        self.assertEqual(content[-20:], 'for version 3.9!</p>')

    def test_contains_text_before_p(self):
        """Tests that text in the outer div before a p is retained."""
        html = '<div>this is valuable text<p>and here is more</p></div>'
        self.assertTrue(contains_text(etree.fromstring(html)))

    def test_contains_text_between_p(self):
        """Tests that text in the outer div before a p is retained."""
        html = '''
        <div><p>This is text. </p>This is valuable text<p>and
        here is more</p></div>
        '''
        self.assertTrue(contains_text(etree.fromstring(html)))

    def test_contains_text_after_p(self):
        """Tests that text in the outer div before a p is retained."""
        html = '<div><p>This is text. </p>This is valuable text.</div>'
        self.assertTrue(contains_text(etree.fromstring(html)))

    def test_cleanup_and_text_between_children(self):
        """
        Tests that cleanup maintains text between children of enclosing
        div.
        """
        html = '<div>text <p>text </p>text <p>text </p>text</div>'
        target = 'text <p>text </p>text <p>text </p>text'
        self.assertEqual(elem_content_to_string(
            cleanup(etree.fromstring(html))), target)

    def test_title_handling(self):
        """
        Tests that, if a title is given when calling Article, the extracted
        title is only accepted if it is contained in the given title. This
        is for the usage scenario of urls coming from news feeds, etc. where
        the title might be known - even if it contains the site name.
        """
        html = '''
        <html><body>
        <div><h1>Blog Title: Blog Post</h1></div>
        <div id="main">
        <p>This is the main text to be extracted.</p>
        </div>
        </body></html>
        '''
        title = 'Blog Post'
        article_title, content = extract_article(html, title)
        self.assertEqual('<p>This is the main text to be extracted.</p>',
                         content)
        self.assertEqual(title, article_title)

    def test_elem_without_text(self):
        """
        There was a bug that tried to strip from a None object because there
        was no text attribute to the last element in the html tree, as in this
        example. This test checks for that.
        """
        html = """
        <div><div class="articletext">
        <img src="http://www.example.com/image.png" alt="image alt text"/>
        <div class="abstract"><p>The abstract goes here.</p></div>
        <p> </p>
        <p><b>Some bold text.</b><br/>&#13;
        <br/>&#13;
        This here is a part of the text to be extracted. It is a bit longer
        than the other lines and parts.<br/>&#13;
        <br/>&#13;
        Just some text.<br/>&#13;
        <br/>&#13;
        Text <a href="http://www.example.com" title="external link" \
        target="_blank" class="nosymbol">http://www.example.com</a></p>
        </div>
        </div>
        """
        cleanup(etree.fromstring(html))
        start = '<img src="'
        end = 'om</a></p>'
        self.assertEqual(elem_content_to_string(
            cleanup(etree.fromstring(html)))[:10], start)
        self.assertEqual(elem_content_to_string(
            cleanup(etree.fromstring(html)))[-10:], end)
