from django.conf.urls import url, include
from django.urls import reverse_lazy
from django.conf.urls.static import static
from django.conf import settings

from cms.views.sitemap import CategoriesSitemap, PostsSitemap, StaticSitemap
from cms.views import post, ajax, comment, profile, map, registration

from cms.forms.registration import RememberAuthenticationForm
from django.contrib.sitemaps.views import sitemap
from django.contrib.auth import views as auth_views

from cms.views.rss import LatestEntriesFeed

sitemaps = {
    'categories': CategoriesSitemap,
    'static': StaticSitemap,
    'posts': PostsSitemap,
}

urlpatterns = [
    url(r'^$', post.post_list, name='post_list'),
    url(r'^post/new/$', post.post_new, name='post_new'),
    url(r'^post/(?P<pk>[0-9]+)/$', post.post_detail, name='post_detail'),

    url(r'^post/(?P<pk>[0-9]+)/edit/$', post.post_edit, name='post_edit'),
    url(r'^post/(?P<pk>[0-9]+)/delete/$', post.post_delete, name='post_delete'),

    url(r'^post/(?P<pk>[0-9]+)/comment/new/$', comment.comment_new, name='comment_new'),
    url(r'^post/(?P<pk>[0-9]+)/comment(?P<cpk>[0-9]+)/reply/$', comment.comment_reply, name='comment_reply'),
    url(r'^post/(?P<pk>[0-9]+)/comment(?P<cpk>[0-9]+)/edit/$', comment.comment_edit, name='comment_edit'),
    url(r'^post/(?P<pk>[0-9]+)/comment(?P<cpk>[0-9]+)/delete/$', comment.comment_delete, name='comment_delete'),

    url(r'^author/(?P<author>\w+)?/$', post.post_list, name='author_list'),
    url(r'^author/(?P<author>\w+)/tags/(?P<tags>[\w\s\d\-_,]+)?/$', post.post_list, name='author_tags_list'),

    url(r'^category/(?P<category>\w+)?/$', post.post_list, name='category_list'),
    url(r'^category/(?P<category>\w+)/tags/(?P<tags>[\w\s\d\-_,]+)?/$', post.post_list, name='category_tags_list'),

    url(r'^tags/(?P<tags>[\w\s\d\-_,]+)/$', post.post_list, name='tag_list'),

    url(r'^maps/$', map.maps_list, name='maps_list'),
    url(r'^maps/new/$', map.map_new, name='map_new'),
    url(r'^maps/(?P<pk>[0-9]+)/$', map.serve_map_file, name='map_file'),
    url(r'^maps/(?P<pk>[0-9]+)/edit/$', map.map_edit, name='map_edit'),
    url(r'^maps/(?P<pk>[0-9]+)/delete/$', map.map_delete, name='map_delete'),

    url(r'^maps/author/(?P<author>\w+)?/$', map.maps_list, name='maps_author_list'),
    url(r'^maps/author/(?P<author>\w+)/tags/(?P<tags>[\w\s\d\-_,]+)?/$', map.maps_list, name='maps_author_tags_list'),

    url(r'^maps/tags/(?P<tags>[\w\s\d\-_,]+)/$', map.maps_list, name='maps_tag_list'),

    url(r'^accounts/login/$', registration.remember_login, {
        'template_name': 'registration/login.html',
        'authentication_form': RememberAuthenticationForm
    }, name='auth_login'),
    url(r'^accounts/logout/$', auth_views.LogoutView.as_view(next_page=reverse_lazy('post_list')),
        name='auth_logout'),

    url(r'^accounts/register/$', registration.registration, name='registration_register'),
    url(r'^accounts/register/complete/$', registration.profile, name='registration_complete'),
    url(r'^accounts/register/confirm/(?P<activation_key>[-:\w]+)/$', registration.activation,
        name='registration_confirm'),
    url(r'^accounts/register/send_confirm/$', registration.send_activation,
        name='registration_send_confirm'),

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

    url(r'^accounts/email/change/$', registration.edit_email, name='auth_email_change'),
    url(r'^accounts/email/change/done/(?P<uidb64>[0-9A-Za-z_\-]+)/'
        r'(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', registration.edit_email_done, name='auth_email_change_done'),

    url(r'^accounts/me/$', profile.my_profile, name='me'),
    url(r'^accounts/me/edit/$', profile.profile_edit, name='me_edit'),
    url(r'^accounts/user/(?P<username>\w+)/$', profile.profile, name='user'),
    url(r'^accounts/user/(?P<username>\w+)/edit/$', profile.profile_edit, name='user_edit'),
    url(r'^accounts/userlist/$', profile.userlist, name='users_list'),

    url(r'^upload/', post.upload, name='ckeditor_upload'),

    url(r'^ajax/tags/', ajax.get_simular_tags, name="get_simular_tags"),

    url(r'^messages/', include('django_messages.urls')),

    url(r'^sitemap\.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    url(r'^latest/feed/', LatestEntriesFeed(), name="feed_latest"),
    url(r'^webpush/', include('webpush.urls')),
    url('', include('social_django.urls', namespace='social'))
]

if settings.ENV == 'development':
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
