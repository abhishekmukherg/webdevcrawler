import httplib
import urllib2

import mox

from django.test import TestCase

from webdevcrawler.crawler import helpers
from webdevcrawler.crawler.models import Url, HeadRequest


class TestUrlCrawlString(TestCase):

    def test_simple(self):
        string='<!DOCTYPE html><a href="http://www.google.com">foo</a>'
        u = Url(href='http://foo.bar.com')
        r = u._crawl_string(string)
        self.assertEqual(len(r), 1)
        self.failUnless('http://www.google.com' in r, r)
        self.assertEqual(r['http://www.google.com'], set(['foo']))

    def test_a_title(self):
        string= \
            '<!DOCTYPE html><a href="http://www.google.com" title="foo"></a>'
        u = Url(href='http://foo.bar.com')
        r = u._crawl_string(string)
        self.assertEqual(len(r), 1)
        self.failUnless('http://www.google.com' in r, r)
        self.assertEqual(r['http://www.google.com'], set(['foo']))

    def test_a_img(self):
        string= """<!DOCTYPE html>
        <a href="http://www.google.com"><img alt="foo"/></a>'
        """
        u = Url(href='http://foo.bar.com')
        r = u._crawl_string(string)
        self.assertEqual(len(r), 1)
        self.failUnless('http://www.google.com' in r, r)
        self.assertEqual(r['http://www.google.com'], set(['foo']))

    def test_combined(self):
        string = """<!DOCTYPE html>
        <a href="http://www.google.com" title="foo"><img alt="bar"/></a>
        """
        u = Url(href='http://foo.bar.com')
        r = u._crawl_string(string)
        self.assertEqual(len(r), 1)
        self.failUnless('http://www.google.com' in r, r)
        self.assertEqual(r['http://www.google.com'],
                set(['foo', 'bar']))

    def test_multiple_url(self):
        string = """<!DOCTYPE html>
        <a href="http://www.google.com" title="foo"><img alt="bar"/></a>
        <a href="http://www.froogle.com" title="foo"><img alt="bar"/></a>
        """
        u = Url(href='http://foo.bar.com')
        r = u._crawl_string(string)
        self.assertEqual(len(r), 2)
        self.failUnless('http://www.google.com' in r, r)
        self.failUnless('http://www.froogle.com' in r, r)
        self.assertEqual(r['http://www.google.com'],
                set(['foo', 'bar']))
        self.assertEqual(r['http://www.froogle.com'],
                set(['foo', 'bar']))

class TestUrlCrawlUrl(TestCase):

    def setUp(self):
        self.mox = mox.Mox()

    def tearDown(self):
        self.mox.UnsetStubs()

    def test_invalid_content_type(self):
        self.mox.StubOutWithMock(urllib2, 'urlopen')
        url = 'http://www.google.com'
        info = self.mox.CreateMock(httplib.HTTPMessage)
        info.getheader('content-type').AndReturn('text/png')
        addinfo = self.mox.CreateMock(urllib2.addinfourl)
        addinfo.info().AndReturn(info)
        urllib2.urlopen(mox.IsA(HeadRequest)).AndReturn(addinfo)
        self.mox.ReplayAll()

        u = Url(href=url)
        result = u.crawl_url()

        self.mox.VerifyAll()
        self.assertEqual(result, False)


