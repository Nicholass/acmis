from django.conf.urls import url, include
from . import views
from django.contrib.auth import views as auth_views

from django.urls import reverse_lazy

urlpatterns = [
  url(r'^$', views.post_list, name='post_list'),
  url(r'^post/(?P<pk>[0-9]+)/$', views.post_detail, name='post_detail'),

  url(r'^i18n/', include('django.conf.urls.i18n')),
  url(r'^category/(?P<category>\w+)/new/$', views.post_new, name='post_new'),
  url(r'^post/(?P<pk>[0-9]+)/edit/$', views.post_edit, name='post_edit'),
  url(r'^post/(?P<pk>[0-9]+)/delete/$', views.post_delete, name='post_delete'),

  url(r'^post/(?P<pk>[0-9]+)/comment/new/$', views.comment_new, name='comment_new'),
  url(r'^post/(?P<pk>[0-9]+)/comment(?P<cpk>[0-9]+)/reply/$', views.comment_reply, name='comment_reply'),
  url(r'^post/(?P<pk>[0-9]+)/comment(?P<cpk>[0-9]+)/edit/$', views.comment_edit, name='comment_edit'),
  url(r'^post/(?P<pk>[0-9]+)/comment(?P<cpk>[0-9]+)/delete/$', views.comment_delete, name='comment_delete'),

  url(r'^author/(?P<author>\w+)?/$', views.post_list, name='author_list'),
  url(r'^author/(?P<author>\w+)/tags/(?P<tags>[\w\s\d\-_,]+)?/$', views.post_list, name='author_tags_list'),

  url(r'^category/(?P<category>\w+)?/$', views.post_list, name='category_list'),
  url(r'^category/(?P<category>\w+)/tags/(?P<tags>[\w\s\d\-_,]+)?/$', views.post_list, name='category_tags_list'),

  url(r'^tags/(?P<tags>[\w\s\d\-_,]+)/$', views.post_list, name='tag_list'),

  url(r'^map/(?P<map_hash>\w+)/$', views.serve_map_file, name='map_file'),

  # Fixed django-registration urls
  # TODO: Remove after fix in next versions of package
  # https://github.com/ubernostrum/django-registration/issues/106
  # https://github.com/ubernostrum/django-registration/pull/111
  url(r'^accounts/password/change/$',
      auth_views.PasswordChangeView.as_view(
          success_url=reverse_lazy('auth_password_change_done')
      ),
      name='auth_password_change'),
  url(r'^accounts/password/change/done/$',
      auth_views.PasswordChangeDoneView.as_view(),
      name='auth_password_change_done'),
  url(r'^accounts/password/reset/$',
      auth_views.PasswordResetView.as_view(
          success_url=reverse_lazy('auth_password_reset_done')
      ),
      name='auth_password_reset'),
  url(r'^accounts/password/reset/complete/$',
      auth_views.PasswordResetCompleteView.as_view(),
      name='auth_password_reset_complete'),
  url(r'^accounts/password/reset/done/$',
      auth_views.PasswordResetDoneView.as_view(),
      name='auth_password_reset_done'),
  url(r'^accounts/password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/'
      r'(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(
            success_url=reverse_lazy('auth_password_reset_complete')
        ),
        name='auth_password_reset_confirm'),

  url(r'^accounts/', include('registration.backends.hmac.urls')),
]
