from django.conf.urls import patterns, include, url
from django.contrib import admin
from . import settings
import os

urlpatterns = patterns('',
    url(r'^site/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': 'static/output' if settings.DEBUG\
                                         else os.path.join(settings.STATIC_ROOT,
                                                           'output')
    }),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^tinymce/', include('tinymce.urls')),
)
