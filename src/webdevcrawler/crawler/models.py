import urllib2
import time
import urlparse
import collections
import sys
import logging

from django.db import models, backend

import BeautifulSoup


logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


def add_keepalive():
    try:
        import urlgrabber.keepalive
    except ImportError:
        log.info("Could not find urlgrabber, using default opener")
        pass
    else:
        log.info("Using keepalive handler to get urls")
        keepalive_handler = urlgrabber.keepalive.HTTPHandler()
        opener = urllib2.build_opener(keepalive_handler)
        urllib2.install_opener(opener)
add_keepalive()


class HeadRequest(urllib2.Request):
    def get_method(self):
        return "HEAD"


class Url(models.Model):

    href = models.URLField(verify_exists=True, unique=True, db_index=True)
    excluded = models.BooleanField(default=False)
    etag = models.CharField(max_length=32, null=True)

    def __unicode__(self):
        return unicode(self.href)

    class Meta:
        app_label = 'crawler'

    def crawl_url(self):
        """Crawl url and return a dictionary of urls to a list of keywords

        Tries to crawl url, if etag is specified and the resources etag
        is equal, return False

        """
        try:
            u = urllib2.urlopen(HeadRequest(self.href))
        except urllib2.URLError, urllib2.BadStatusLine:
            return
        ct = u.info().getheader('content-type')
        if 'text/html' not in ct:
            log.debug("Not html, quitting")
            return False
        etag = u.info().getheader('etag')
        if self.etag is not None:
            if etag == self.etag:
                log.debug("Etag equal, exiting")
                return False
        log.debug("Fetched etag {0}, had etag {1}".format(etag, self.etag))
        self.etag = etag
        return self._crawl_string(urllib2.urlopen(self.href))

    def _crawl_string(self, string):
        try:
            soup = BeautifulSoup.BeautifulSoup(string)
        except BeautifulSoup.HTMLParseError:
            return False
        if soup is None:
            return False
        url_keywords = collections.defaultdict(set)
        for a_tag in soup.findAll('a'):
            if not a_tag.has_key('href'):
                continue
            href = unicode(urlparse.urljoin(self.href, a_tag['href']))
            if a_tag.has_key('alt'):
                url_keywords[href].add(a_tag['alt'])
            contents = a_tag.string
            if contents is None:
                if a_tag.img is not None and a_tag.img.has_key('alt'):
                    contents = a_tag.img['alt']
            if contents is None:
                continue
            url_keywords[href].add(contents)
        return url_keywords



class Keyword(models.Model):

    word = models.CharField(max_length=128, unique=True, db_index=True)
    urls = models.ManyToManyField(Url)

    def __unicode__(self):
        return unicode(self.word)

    class Meta:
        app_label = 'crawler'


