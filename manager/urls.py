from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('',
    url(r'(?P<path>.*)$', 'django.views.static.serve')
)
