from django.conf.urls import url, include
from . import views

urlpatterns = [
  url(r'^$', views.post_list, name='post_list'),
  url(r'^post/(?P<pk>[0-9]+)/$', views.post_detail, name='post_detail'),

  url(r'^i18n/', include('django.conf.urls.i18n')),
  url(r'^category/(?P<category>\w+)/new/$', views.post_new, name='post_new'),
  url(r'^post/(?P<pk>[0-9]+)/edit/$', views.post_edit, name='post_edit'),
  url(r'^post/(?P<pk>[0-9]+)/delete/$', views.post_delete, name='post_delete'),

  url(r'^author/(?P<author>\w+)?/$', views.post_list, name='author_list'),
  url(r'^author/(?P<author>\w+)/tags/(?P<tags>[\w\s\d\-_,]+)?/$', views.post_list, name='author_tags_list'),
  url(r'^category/(?P<category>\w+)?/$', views.post_list, name='category_list'),
  url(r'^category/(?P<category>\w+)/tags/(?P<tags>[\w\s\d\-_,]+)?/$', views.post_list, name='category_tags_list'),
  url(r'^tags/(?P<tags>[\w\s\d\-_,]+)/$', views.post_list, name='tag_list'),
]
