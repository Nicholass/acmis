from django.core.management.base import NoArgsCommand
from punbb.authent.models import PunbbGroup, PunbbUser
from django.contrib.auth.models import User, Group

class Command(NoArgsCommand):
    help = 'Imports  punbb users and groups; adds "punbb" group to imported users.'

    requires_model_validation = False

    def handle_noargs(self, **options):
        for g in PunbbGroup.objects.all():
            dg , created = Group.objects.get_or_create(name=g.g_title)
            if created: print 'group', dg.name, 'created.'
        gpunbb, c = Group.objects.get_or_create(name='punbb')
        for u in PunbbUser.objects.all():
            lresult = User.objects.filter(username=u.username)
            if len(lresult) == 0:
                du = User.objects.create_user(u.username, u.email)
                print 'user', u.username, 'imported.'
                if u.realname:
                    du.last_name = u.realname
                    du.save()
            else:
                du = lresult[0]
            if not gpunbb in du.groups.all():
                du.groups.add(gpunbb)
                print '  group punbb added to user', du.username
            
