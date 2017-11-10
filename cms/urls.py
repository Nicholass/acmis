from django.conf.urls import url
from . import views

urlpatterns = [
  url(r'^$', views.post_list, name='post_list'),
  url(r'^author/(?P<author>\w+)/?(?P<tag>\w+)?/$', views.post_list, name='author_list'),
  url(r'^category/(?P<category>\w+)/?(?P<tag>\w+)?/$', views.post_list, name='category_list'),
  url(r'^tag/(?P<tag>\w+)/$', views.post_list, name='tag_list'),


  url(r'^post/(?P<pk>[0-9]+)/$', views.post_detail, name='post_detail'),
  url(r'^category/(?P<category>\w+)/new/$', views.post_new, name='post_new'),
  url(r'^post/(?P<pk>[0-9]+)/edit/$', views.post_edit, name='post_edit'),
]
