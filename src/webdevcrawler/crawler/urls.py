from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:

urlpatterns = patterns('webdevcrawler.crawler.views',
    (r'^crawl/', 'crawl'),
)
