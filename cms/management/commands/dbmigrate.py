from django.core.management.base import BaseCommand

from cms.models.comment import Comment
from cms.models.cmscategory import CmsCategory
from cms.models.cmspost import CmsPost
from cms.models.cmsprofile import CmsProfile
from cms.models.map import Map
from django.contrib.auth.models import User

import psycopg2

class Command(BaseCommand):
    help = 'Migrate from db old to db actiual'


    def handle(self, *args, **options):
        conn = psycopg2.connect(dbname='diggers_old', user='diggers',
                                password='Ed4sTJHJ5ihF7puS', host='localhost')
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        ### Add user profiles

        cursor.execute('SELECT * FROM cms_cmsprofile WHERE TRUE')
        for profile in cursor:
            user = User.objects.get(id=profile['user_id'])
            existing_profile = CmsProfile.objects.filter(user=user).count()

            if existing_profile:
                continue

            CmsProfile.objects.create(
                user=user,
                avatar=profile['avatar'],
                birth_date=profile['birth_date'],
                location=profile['location'],
                vk=profile['vk'],
                instagram=profile['instagram'],
                telegram=profile['telegram'],
                last_activity=profile['last_activity'],
                email_verefied=True
            )
            print('Created profile for user %s' % user.username)

        ### Add posts

        cursor.execute('SELECT * FROM cms_cmspost WHERE TRUE')
        posts = cursor.fetchall()

        for post in posts:
            author = User.objects.get(id=post[5])
            category = None

            cursor.execute('SELECT '
                           'taggit_tag.name '
                           'FROM taggit_taggeditem '
                           'LEFT JOIN taggit_tag ON taggit_taggeditem.tag_id=taggit_tag.id '
                           'WHERE taggit_taggeditem.object_id=%d' % post[0])
            tags = cursor.fetchall()

            existing_post = CmsPost.objects.filter(title=post[1]).count()

            # If binary post
            if post[7] == 16:
                cursor.execute('SELECT * FROM cms_binarypost WHERE cmspost_ptr_id=%d' % post[0])
                post_content = cursor.fetchone()

                # If map
                if post[6] == 2:
                    existing_post = Map.objects.filter(title=post[1]).count()
                    if existing_post:
                        continue

                    new_map = Map.objects.create(
                        title=post[1],
                        author=author,
                        created_date=post[2],
                        description=post_content[2],
                        file=post_content[1],
                    )

                    for tag in tags:
                        new_map.tags.add(tag['name'])

                    print('Post %s converted to map' % post[1])
                    continue

                # If picture
                if existing_post:
                    continue

                if post[6] == 1:
                    category = CmsCategory.objects.get(route='creative')

                if post[6] == 4:
                    category = CmsCategory.objects.get(route='photo')

                new_post = CmsPost.objects.create(
                    title=post[1],
                    author=author,
                    category=category,
                    created_date=post[2],
                    text='<p><img src="/media/%s" alt="Забраження поста" /></p>' % post_content[1],
                )

                for tag in tags:
                    new_post.tags.add(tag['name'])

                print('Post %s converted to category %s' % (post[1], category.name,))
                continue

            # If binary post
            if post[7] == 17:
                if existing_post:
                    continue

                cursor.execute('SELECT * FROM cms_textpost WHERE cmspost_ptr_id=%d' % post[0])
                post_content = cursor.fetchone()

                if post[6] == 3:
                    category = CmsCategory.objects.get(route='news')

                if post[6] == 5:
                    category = CmsCategory.objects.get(route='creative')

                if post[6] == 6:
                    category = CmsCategory.objects.get(route='reports')

                new_post = CmsPost.objects.create(
                    title=post[1],
                    author=author,
                    category=category,
                    created_date=post[2],
                    text=post_content[1],
                )

                for tag in tags:
                    new_post.tags.add(tag['name'])

                print('Post %s added to category %s' % (post[1], category.name,))

        ### Add comments

        cursor.execute('SELECT * FROM cms_comment WHERE TRUE ORDER BY id ASC')
        comments = cursor.fetchall()

        for comment in comments:
            cursor.execute('SELECT title FROM cms_cmspost WHERE id = %d' % comment[12])
            original_post = cursor.fetchone()

            post = CmsPost.objects.get(title=original_post[0])
            author = User.objects.get(id=comment[10])
            parent = None
            if comment[11]:
                cursor.execute('SELECT text FROM cms_comment WHERE id = %d' % comment[11])
                original_parent = cursor.fetchone()
                parent = Comment.objects.get(text=original_parent[0])

            existing_comment = Comment.objects.filter(text=comment[1])
            if existing_comment:
                continue

            Comment.objects.create(
                text=comment[1],
                is_deleted=comment[3],
                created_date=comment[4],
                modifed_date=comment[5],
                author=author,
                parent=parent,
                post=post,
            )
            print('Created comment from %s' % author)

        cursor.close()
        conn.close()