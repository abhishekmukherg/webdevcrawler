import urlparse
import collections
import logging

from django.db.models import Max

from BeautifulSoup import BeautifulSoup

from webdevcrawler.crawler.models import Url, Keyword


log = logging.getLogger(__name__)


def make_urls_keywords(url, limit_domain):
    class UrlManager(object):
        def __init__(self):
            self._visited_url = set()
            self._unvisited_url = set()
        def add(self, url):
            if url in self._visited_url:
                return
            self._unvisited_url.add(url)
        def pop(self):
            x = self._unvisited_url.pop()
            self._visited_url.add(x)
            return x
        def __len__(self):
            return len(self._unvisited_url)
    url_manager = UrlManager()
    url_manager.add(url)
    while url_manager:
        url = url_manager.pop()
        log.debug("Doing {0}".format(url))
        try:
            url = Url.objects.get(href=url)
        except Url.DoesNotExist:
            log.debug("Making url")
            url = Url(href=url)
        results = url.crawl_url()
        url.save()
        if not results:
            log.debug("No results returned from crawl_url")
            continue
        for href, keywords in results.iteritems():
            # Make sure all the keywords are in the db
            if limit_domain is not None and \
                    not urlparse.urlsplit(href)[1].endswith(limit_domain):
                continue
            url_manager.add(href)
            keyword_obj = []
            for keyword in keywords:
                keyword = keyword.lower()
                try:
                    m = Keyword.objects.get(word=keyword)
                except Keyword.DoesNotExist:
                    m = Keyword(word=keyword)
                    m.save()
                keyword_obj.append(m)
            # Get url
            try:
                url = Url.objects.get(href=href)
            except Url.DoesNotExist:
                url = Url(href=href)
                url.save()
            # add keywords
            for kw in keyword_obj:
                url.keyword_set.add(kw)
            url.save()
    return True
