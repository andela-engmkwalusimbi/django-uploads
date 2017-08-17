from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from api import views

urlpatterns = [
    url(r'^$', views.api_root),
    url(r'^uploads/$', views.FileListView.as_view(), name='files-list'),
    url(r'^uploads/(?P<pk>[0-9]+)/$', views.FileDetailView.as_view(), name='file-details'),
    url(r'^uploads/files$', views.FileSearchView.as_view(), name='files-search'),
]

urlpatterns = format_suffix_patterns(urlpatterns)