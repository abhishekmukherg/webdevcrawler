"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
from webdevcrawler.crawler import helpers

class TestCrawler(TestCase):

    def test_regular_url(self):
        x = helpers._crawl_string('<a href="foo.html">bar</a>',
                'http://www.foo.bar.com')
        self.assertEqual(x.keys(),
                [u'http://www.foo.bar.com/foo.html'])
        self.assertEqual(x.values(), [set([u'bar'])])

    def test_alt_url(self):
        x = helpers._crawl_string('<a href="foo.html" alt="bar" />',
                'http://www.foo.bar.com')
        self.assertEqual(x.keys(),
                [u'http://www.foo.bar.com/foo.html'])
        self.assertEqual(x.values(), [set([u'bar'])])

    def test_img_url(self):
        x = helpers._crawl_string("""
        <a href="foo.html">
          <img src="foo.png" alt="bar" />
        </a>
        """, 'http://www.foo.bar.com')
        self.assertEqual(x.keys(),
                [u'http://www.foo.bar.com/foo.html'])
        self.assertEqual(x.values(), [set([u'bar'])])

    def test_alt_and_img_url(self):
        x = helpers._crawl_string("""
        <a href="foo.html" alt="bar">
          <img src="foo.png" alt="baz" />
        </a>
        """, 'http://www.foo.bar.com')
        self.assertEqual(x.keys(),
                [u'http://www.foo.bar.com/foo.html'])
        self.assertEqual(x.values(), [set([u'bar', u'baz'])])

    def test_multiple_url(self):
        x = helpers._crawl_string("""
        <a href="foo.html">bar</a>
        <a href="foo.html">baz</a>
        """, 'http://www.foo.bar.com')
        self.assertEqual(x.keys(),
                [u'http://www.foo.bar.com/foo.html'])
        self.assertEqual(x.values(), [set([u'bar', u'baz'])])
