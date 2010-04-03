# Create your views here.
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import user_passes_test
from webdevcrawler.crawler.forms import CrawlForm
from django.template import RequestContext

@user_passes_test(lambda u: u.is_staff)
def crawl(request):
    if request.method == 'POST':
        form = CrawlForm(request.POST)
        if form.is_valid():
            return HttpResponse(200)
    else:
        form = CrawlForm()
    return render_to_response('crawler/crawl.html',
            { 'form': form, },
            context_instance=RequestContext(request),
        )
