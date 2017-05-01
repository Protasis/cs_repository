from django.conf.urls import url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^project/(?P<project_id>[0-9]+)/(?P<project_slug>[\w]+)/$', views.project, name='project'),
    url(r'^project/data/(?P<project_id>[0-9]+)$', views.protected_data, {'file_root': settings.DATA_FOLDER}, name='protected_data'),
    # url(r'^{}(?P<path>.*)$'.format(settings.DATA_URL[1:]), views.protected_data, {'file_root': settings.DATA_FOLDER}),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
