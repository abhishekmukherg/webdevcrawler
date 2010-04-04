import urllib2

from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseForbidden
from django.shortcuts import render_to_response, redirect
from django.template import loader
from django.template import RequestContext

from BeautifulSoup import BeautifulSoup

from webdevcrawler.crawler.forms import CrawlForm
from webdevcrawler.crawler import helpers
from webdevcrawler.crawler.models import Url, Keyword
from webdevcrawler import settings

def crawl(request):
    # Make sure we're logged in
    if not request.user.is_authenticated():
        return redirect(settings.LOGIN_URL)
    # And have the right privs
    elif (not request.user.is_staff or
            not request.user.has_perm('crawler.add_url') or
            not request.user.has_perm('crawler.add_keyword')):
        return render_to_response('crawler/403.html',{},
                context_instance=RequestContext(request))
        l = loader.render_to_string('crawler/403.html',
                context_instance=RequestContext(request))
        return HttpResponseForbidden(l)
    # Process forms
    if request.method == 'POST':
        form = CrawlForm(request.POST)
        if form.is_valid():
            results = helpers.crawl_url(form.cleaned_data['url'])
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
            raise False
    else:
        form = CrawlForm()
    return render_to_response('crawler/crawl.html',
            { 'form': form, },
            context_instance=RequestContext(request),
        )
