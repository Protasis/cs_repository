from django.conf.urls import url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

from wiki.urls import get_pattern as get_wiki_pattern
from django_nyt.urls import get_pattern as get_nyt_pattern

from . import views

urlpatterns = [
    url(r'^notifications/', get_nyt_pattern()),
    url(r'^wiki/', get_wiki_pattern(), name='wiki'),
    url(r'^$', views.index, name='index'),
    url(r'^(?P<cl>data)/(?P<hash>[0-9A-F]{128})/(?P<filename>[\w]+)', views.get, name='get_data'),
    url(r'^(?P<cl>[\w]+)/(?P<id>[0-9]+)/(?P<slug>[\w]+)/$', views.get, name='get_check'),
    # url(r'^project/(?P<project_id>[0-9]+)/(?P<project_slug>[\w]+)/$', views.project, name='project'),
    # url(r'^whitepaper/(?P<paper_id>[0-9]+)/(?P<paper_slug>[\w]+)/$', views.paper, name='paper'),
    # url(r'^paper/data/(?P<paper_id>[0-9]+)$', views.protected_data, name='protected_data'),
    # url(r'^{}(?P<path>.*)$'.format(settings.DATA_URL[1:]), views.protected_data, {'file_root': settings.DATA_FOLDER}),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
