import uuid
import datetime

from django.utils import timezone
from django.contrib.auth.signals import user_logged_out, user_logged_in
from django.core.cache import cache
from django.conf import settings
from django.template.response import TemplateResponse

from django.contrib.auth.models import User
from django.utils.deprecation import MiddlewareMixin

ONLINE_THRESHOLD = getattr(settings, 'USER_ONLINE_TIMEOUT', 60 * 15)


def remove_user_id(sender, user, request, **kwargs):
    uids = cache.get('online-users', [])
    if user.id in uids:
        uids.remove(user.id)
    cache.set('online-users', uids, ONLINE_THRESHOLD)


user_logged_out.connect(remove_user_id)


def remove_anon_id(sender, user, request, **kwargs):
    aids = cache.get('online-guests', [])
    aid = request.COOKIES.get('aid')
    if aid and aid in aids:
        aids.remove(aid)
        cache.set('online-guests', aids, ONLINE_THRESHOLD)


user_logged_in.connect(remove_anon_id)


class OnlineUsersMiddleware(MiddlewareMixin):
    aid = None

    def get_online_now(self, uids):
        return User.objects.filter(id__in=uids or [])

    def process_request(self, request):
        uids = cache.get('online-users', [])
        aids = cache.get('online-guests', [])

        if request.user.is_authenticated():
            uid = request.user.id

            if not uid in uids:
                uids.append(uid)

        else:
            self.aid = request.COOKIES.get('aid')

            if not self.aid:
                self.aid = str(uuid.uuid4())

            if not self.aid in aids:
                aids.append(self.aid)

        # Attach our modifications to the request object
        request.__class__.online_users = uids
        request.__class__.online_guests = aids
        request.__class__.online_now = self.get_online_now(uids)

        # Set the new cache
        cache.set('online-users', uids, ONLINE_THRESHOLD)
        cache.set('online-guests', aids, ONLINE_THRESHOLD)

    def process_response(self, request, response):
        if not request.user.is_authenticated():
            expires = datetime.datetime.strftime(
                datetime.datetime.utcnow() + datetime.timedelta(seconds=ONLINE_THRESHOLD),
                "%a, %d-%b-%Y %H:%M:%S GMT")
            response.set_cookie('aid', self.aid, max_age=ONLINE_THRESHOLD, expires=expires,
                                domain=settings.SESSION_COOKIE_DOMAIN,
                                secure=settings.SESSION_COOKIE_SECURE or None)
        else:
            response.delete_cookie('aid')

        return response


class ActiveUserMiddleware(MiddlewareMixin):

    def process_request(self, request):
        current_user = request.user
        if request.user.is_authenticated():
            user = User.objects.get(pk=current_user.pk)
            user.profile.last_activity = timezone.now()
            user.save()


class XForwardedForMiddleware(MiddlewareMixin):

    def process_request(self, request):
        if ("HTTP_X_FORWARDED_FOR") in request.META:
            request.META["HTTP_X_PROXY_REMOTE_ADDR"] = request.META["REMOTE_ADDR"]
            parts = request.META["HTTP_X_FORWARDED_FOR"].split(",", 1)
            request.META["REMOTE_ADDR"] = parts[0]

class BanManagement(MiddlewareMixin):

    def process_response(self, request, response):
        current_user = request.user
        if request.user.is_authenticated():
            user = User.objects.get(pk=current_user.pk)

            if user.profile.is_banned:
                response = TemplateResponse(request, 'cms/you_banned.html')
                response._is_rendered = False
                response.render()

        return response
