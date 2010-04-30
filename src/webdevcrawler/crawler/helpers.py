import urlparse
import collections
import logging

from django.db.models import Max

from BeautifulSoup import BeautifulSoup

from webdevcrawler.crawler.models import Url, Keyword


log = logging.getLogger(__name__)


class _UrlManager(object):
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


def _get_or_create(cls, save=False, *args, **kwargs):
    try:
        obj = cls.objects.get(*args, **kwargs)
    except cls.DoesNotExist:
        obj = cls(*args, **kwargs)
        if save:
            obj.save()
    return obj


def _process_url(url_manager, limit_domain):
    base_url_href = url_manager.pop()
    log.debug("Doing {0}".format(base_url_href))
    base_url = _get_or_create(Url, href=base_url_href)
    results = base_url.crawl_url()
    base_url.save()

    if not results:
        log.debug("No results returned from crawl_url")
        return

    for href, keywords in results.iteritems():
        # Make sure all the keywords are in the db
        if limit_domain is not None and \
                not urlparse.urlsplit(href)[1].endswith(limit_domain):
            continue
        url_manager.add(href)
        url = _get_or_create(Url, save=True, href=href)

        for keyword in keywords:
            keyword = keyword.lower()
            m = _get_or_create(Keyword, save=True, word=keyword)
            url.keyword_set.add(m)
        url.save()


def make_urls_keywords(url, limit_domain):
    url_manager = _UrlManager()
    url_manager.add(url)
    while url_manager:
        _process_url(url_manager, limit_domain)
    return True
