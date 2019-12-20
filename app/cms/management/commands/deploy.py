import subprocess
import os
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = 'Deploy base site with default database'


    def handle(self, *args, **options):

        subprocess.call(['python', './manage.py', 'collectstatic'])

        geoip_dir = getattr(settings, 'GEOIP_PATH')
        if not os.path.exists(geoip_dir):
            os.makedirs(geoip_dir)
            self.stdout.write('Created geoip dir "%s"' % geoip_dir)

        subprocess.call(['python', './manage.py', 'install_geoip_dataset'])
        subprocess.call(['python', './manage.py', 'makemigrations'])
        subprocess.call(['python', './manage.py', 'migrate'])
        subprocess.call(['django-admin',  'compilemessages'])


