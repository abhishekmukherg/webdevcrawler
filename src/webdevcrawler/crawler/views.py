try:
    import json
except ImportError:
    import simplejson as json

from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseForbidden, Http404, HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template import loader
from django.template import RequestContext
from django.db.models import Count
from django.db.models import Q

from django.db import transaction
try:
    from django.views.decorators.csrf import csrf_protect
except ImportError:
    csrf_protect = lambda x: x

from webdevcrawler.crawler.forms import CrawlForm
from webdevcrawler.crawler import helpers
from webdevcrawler.crawler import models
from webdevcrawler import settings

@csrf_protect
@transaction.commit_manually
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
            helpers.make_urls_keywords(form.cleaned_data['url'],
                    form.cleaned_data['limit_to_domain'] or None)
            transaction.commit()
    else:
        form = CrawlForm()
    response = render_to_response('crawler/crawl.html',
            { 'form': form, },
            context_instance=RequestContext(request),
        )
    transaction.commit()
    return response

def search(request, limit=10):
    if 'q' not in request.GET:
        raise Http404
    if 'offset' in request.GET:
        limit = int(request.GET['offset']) + 10
        offset = int(request.GET['offset'])
    else:
        offset = 0
        limit = 10
    urls = models.Url.objects.filter(
            Q(keyword__word__icontains=request.GET['q']) |
            Q(title__icontains=request.GET['q']) ).distinct()[offset:limit]
    count = models.Url.objects.filter(
            Q(keyword__word__icontains=request.GET['q']) |
            Q(title__icontains=request.GET['q']) ).distinct().count()
    results = []
    for url in urls:
        for keyword in url.keyword_set.all():
            if request.GET['q'].lower()  in keyword.word.lower() or \
                    request.GET['q'].lower()  in url.title.lower():
                results.append(
                        {"href": url.href,
                            "title": url.title or "",
                            "keyword": keyword.word})
                break
    result = json.dumps({'count': count, 'results': results})
    return HttpResponse('{0}({1})'.format(request.GET['callback'], result))
