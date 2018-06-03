from django.contrib.auth.models import User
from punbb.authent.models import PunbbUsers
from django.conf import settings
import sha


class PunBBShaBackend:
    def __init__(self):
        self.crypter = sha
    def authenticate(self, username=None, password=None):
        try:
            pass_encoded = self.crypter.new(password).hexdigest()
            bbuser = PunbbUsers.objects.get(username__exact=username, password=pass_encoded)
        except Exception:
            return None
        
        # create user in django if not existing
        try:
            user = User.objects.get(username__exact=username)
        except:
            user = User.objects.create_user(username, bbuser.email)
            user.is_staff = settings.EXTERN_USER_IS_STAFF
            user.save()
        return user
    
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
