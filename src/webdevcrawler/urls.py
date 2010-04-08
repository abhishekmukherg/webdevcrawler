from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
        # Example:

        # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
        # to INSTALLED_APPS to enable admin documentation:
        (r'^admin/doc/', include('django.contrib.admindocs.urls')),

        # Uncomment the next line to enable the admin:
        (r'^admin/', include(admin.site.urls)),

        (r'^accounts/login/$', 'django_cas.views.login'),
        (r'^accounts/logout/$', 'django_cas.views.logout'),

        (r'^', include('webdevcrawler.crawler.urls')),
        )

if settings.DEBUG:
    urlpatterns += patterns('',
            (r'^{0}/(?P<path>.*)$'.format(settings.MEDIA_URL.strip('/')),
                'django.views.static.serve',
                {'document_root': settings.MEDIA_ROOT }),
            )

