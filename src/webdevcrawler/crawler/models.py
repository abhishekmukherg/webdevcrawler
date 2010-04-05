import urllib2
import time
import urlparse
import collections
import sys

from django.db import models

from BeautifulSoup import BeautifulSoup


class Url(models.Model):

    href = models.URLField(verify_exists=True, unique=True, db_index=True)
    excluded = models.BooleanField(default=False)
    etag = models.CharField(max_length=32)

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
            u = urllib2.urlopen(self.href)
        except urllib2.URLError:
            return
        etag = u.info().get('ETag')
        if self.etag is not None:
            if etag == self.etag:
                return False
            self.etag = etag
        return self._crawl_string(u)


    def _crawl_string(self, string):
        soup = BeautifulSoup(string)
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
