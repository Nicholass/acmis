from django.core.management.base import BaseCommand

import psycopg2

class Command(BaseCommand):
    help = 'Migrate from db old to db actiual'


    def handle(self, *args, **options):
        conn = psycopg2.connect(dbname='diggers_old', user='diggers',
                                password='Ed4sTJHJ5ihF7puS', host='localhost')
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM auth_user WHERE TRUE')

        print(cursor.fetchall())
