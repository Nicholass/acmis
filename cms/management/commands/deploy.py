import subprocess
from django.core.management.base import BaseCommand, CommandError

from cms.models import CmsCategory
from django.contrib.auth.models import User, Group, Permission
from django.contrib.sites.models import Site


class Command(BaseCommand):
    help = 'Deploy base site with default database'


    def handle(self, *args, **options):

        subprocess.call(['python', './manage.py', 'bower', 'install', '--', '--allow-root'])
        subprocess.call(['python', './manage.py', 'collectstatic'])
        subprocess.call(['python', './manage.py', 'makemigrations'])
        subprocess.call(['python', './manage.py', 'migrate'])
        subprocess.call(['python', './manage.py', 'migrate', '--run-syncdb'])

        self.create_superuser()
        self.set_sites()
        self.create_categories()
        self.create_groups()
        self.set_superuser_group()
        self.set_permissions()
        self.set_map_groups()


    def create_superuser(self):
        superuser = User.objects.filter(is_superuser=True)
        if superuser.exists():
            self.stdout.write('Superuser "%s" already exists' % superuser.get().username)
            return

        subprocess.call(['python', './manage.py', 'createsuperuser'])

    def create_groups(self):
        groups = [
            {'name': 'Администраторы'},
            {'name': 'Модераторы'},
            {'name': 'Пользователи с доступом к разделу карт'},
            {'name': 'Пользователи'}
        ]

        for args in groups:
            if not Group.objects.filter(name=args['name']).exists():
                group = Group.objects.create(name=args['name'])
                group.save()

                self.stdout.write('Successfully created group "%s"' % group.name)
            else:
                self.stdout.write('Group "%s" already exists' % args['name'])


    def create_categories(self):
        categories = [
            {'name': 'Drawing', 'route': 'drawing'},
            {'name': 'Map', 'route': 'map'},
            {'name': 'News', 'route': 'news'},
            {'name': 'Photo', 'route': 'photo'},
            {'name': 'Prose', 'route': 'prose'},
            {'name': 'Report', 'route': 'report'}
        ]

        for args in categories:
            if not CmsCategory.objects.filter(name=args['name']).exists():
                category = CmsCategory.objects.create(name=args['name'], route=args['route'])
                category.publish()
                category.save()

                self.stdout.write('Successfully created category "%s"' % category.name)
            else:
                self.stdout.write('CmsCategory "%s" already exists' % args['name'])


    def set_superuser_group(self):
        superusers = User.objects.filter(is_superuser=True)
        admin_group = Group.objects.get(name='Администраторы')
        for user in superusers:
            admin_group.user_set.add(user)
            self.stdout.write('User "%s" added to group "%s"' % (user, admin_group.name))


    def set_permissions(self):
        permissions = {
            'Администраторы': [
                'add_user',
                'change_user',
                'delete_user',
                'add_group',
                'change_group',
                'delete_group',
                'add_tag',
                'change_tag',
                'delete_tag',
                'add_taggeditem',
                'change_taggeditem',
                'delete_taggeditem',
                'add_comment',
                'change_comment',
                'delete_comment',
                'moderate_comment',
                'add_cmspost',
                'change_cmspost',
                'delete_cmspost',
                'moderate_cmspost',
                'publish_cmspost',
                'add_cmscategory',
                'change_cmscategory',
                'delete_cmscategory',
                'change_cmsprofile',
                'moderate_cmsprofile',
                'add_textpost',
                'change_textpost',
                'delete_textpost',
                'moderate_textpost',
                'add_binarypost',
                'change_binarypost',
                'delete_binarypost',
                'moderate_binarypost',
                'add_usersban',
                'change_usersban',
                'delete_usersban',
                'add_emailchange',
                'change_emailchange',
                'delete_emailchange'
            ],
            "Модераторы": [
                'change_user',
                'add_tag',
                'change_tag',
                'delete_tag',
                'add_taggeditem',
                'change_taggeditem',
                'delete_taggeditem',
                'add_comment',
                'change_comment',
                'delete_comment',
                'moderate_comment',
                'add_cmspost',
                'change_cmspost',
                'delete_cmspost',
                'moderate_cmspost',
                'publish_cmspost',
                'change_cmsprofile',
                'moderate_cmsprofile',
                'add_textpost',
                'change_textpost',
                'delete_textpost',
                'moderate_textpost',
                'add_binarypost',
                'change_binarypost',
                'delete_binarypost',
                'moderate_binarypost',
                'add_usersban',
                'change_usersban',
                'delete_usersban',
                'add_emailchange',
                'change_emailchange',
                'delete_emailchange'
            ],
            "Пользователи с доступом к разделу карт": [
                'add_comment',
                'change_comment',
                'delete_comment',
                'add_cmspost',
                'change_cmspost',
                'delete_cmspost',
                'publish_cmspost',
                'add_textpost',
                'change_textpost',
                'delete_textpost',
                'add_binarypost',
                'change_binarypost',
                'delete_binarypost',
                'add_emailchange'
            ],
            "Пользователи": [
                'add_comment',
                'change_comment',
                'delete_comment',
                'add_cmspost',
                'change_cmspost',
                'delete_cmspost',
                'publish_cmspost',
                'add_textpost',
                'change_textpost',
                'delete_textpost',
                'add_binarypost',
                'change_binarypost',
                'delete_binarypost',
                'add_emailchange'
            ]
        }

        groups = Group.objects.all()

        for group in groups:
            if group.name in permissions:
                for perm in permissions[group.name]:
                    permission = Permission.objects.get(codename=perm)
                    group.permissions.add(permission)
                    self.stdout.write('Successfully added permission "%s" for group "%s"' % (permission.codename, group.name,))
            else:
                raise CommandError('No permissions for group "%s"' % group.name)


    def set_map_groups(self):
        groups = [
            "Администраторы",
            "Модераторы",
            "Пользователи с доступом к разделу карт"
        ]

        map_cmscategory = CmsCategory.objects.get(route='map')

        if not map_cmscategory:
            raise CommandError('Map category not exists!')

        map_cmscategory.allow_anonymous = False
        map_cmscategory.save()

        for arg in groups:
            group = Group.objects.get(name=arg)

            if group:
                map_cmscategory.groups.add(group)
                self.stdout.write('Successfully added group "%s" for map category' % group.name)
            else:
                raise CommandError('Group "%s" not exists' % arg)


    def set_sites(self):
        site = Site.objects.get(id=1)
        site.name = 'diggers.kiev.ua'
        site.domain = 'diggers.kiev.ua'
        site.save()

        self.stdout.write('Successfully setup site "%s" with domain "%s"' % (site.name, site.domain,))


