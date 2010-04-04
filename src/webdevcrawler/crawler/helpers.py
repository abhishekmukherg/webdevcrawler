import urlparse
import urllib2
import collections

from BeautifulSoup import BeautifulSoup

from webdevcrawler.crawler.models import Url, Keyword


def make_urls_keywords(url):
    try:
        url = Url.objects.get(href=url)
    except Url.DoesNotExist:
        url = Url(href=url)
    results = url.crawl_url()
    url.save()
    if not results:
        return False
    for href, keywords in results.iteritems():
        # Make sure all the keywords are in the db
        keyword_obj = []
        for keyword in keywords:
            try:
                m = Keyword.objects.get(word=keyword)
            except Keyword.DoesNotExist:
                m = Keyword(word=keyword)
                m.save()
            keyword_obj.append(m)
        try:
            url = Url.objects.get(href=href)
        except Url.DoesNotExist:
            url = Url(href=href)
            url.save()
        for kw in keyword_obj:
            url.keyword_set.add(kw)
        url.save()
    return True
