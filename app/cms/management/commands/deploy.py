import subprocess
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Deploy base site with default database'

    def handle(self, *args, **options):

        subprocess.call(['python', './manage.py', 'collectstatic'])
        subprocess.call(['python', './manage.py', 'makemigrations'])
        subprocess.call(['python', './manage.py', 'migrate'])


