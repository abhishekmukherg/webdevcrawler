import urlparse
import urllib2
import collections

from BeautifulSoup import BeautifulSoup

def crawl_url(url):
    """Crawl url and return a dictionary of urls to a list of keywords"""
    try:
        u = urllib2.urlopen(url)
    except urllib2.URLError:
        return
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

