from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseForbidden
from django.shortcuts import render_to_response, redirect
from django.template import loader
from django.template import RequestContext
try:
    from django.views.decorators.csrf import csrf_protect
except ImportError:
    csrf_protect = lambda x: x

from webdevcrawler.crawler.forms import CrawlForm
from webdevcrawler.crawler import helpers
from webdevcrawler import settings

@csrf_protect
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
    else:
        form = CrawlForm()
    return render_to_response('crawler/crawl.html',
            { 'form': form, },
            context_instance=RequestContext(request),
        )
