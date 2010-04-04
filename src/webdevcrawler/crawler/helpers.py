import urlparse
import urllib2
import collections

from BeautifulSoup import BeautifulSoup

from webdevcrawler.crawler.models import Url, Keyword


def make_urls_keywords(url):
    try:
        url = Url.objects.get(href=url)
    except Url.DoesNotExist:
        etag = None
    else:
        etag = url.etag
    results = crawl_url(url, etag)
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


def crawl_url(url, etag=None):
    """Crawl url and return a dictionary of urls to a list of keywords

    Tries to crawl url, if etag is specified and the resources etag is equal,
    return False

    """
    try:
        u = urllib2.urlopen(url)
    except urllib2.URLError:
        return
    if etag is not None:
        if u.info().get('ETag') == etag:
            return False
    return _crawl_string(u, url)


def _crawl_string(str, url):
    soup = BeautifulSoup(str)
    if soup is None:
        return False
    url_keywords = collections.defaultdict(set)
    for a_tag in soup.findAll('a'):
        if not a_tag.has_key('href'):
            continue
        href = unicode(urlparse.urljoin(url, a_tag['href']))
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

