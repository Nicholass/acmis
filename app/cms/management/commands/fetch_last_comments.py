from django.core.management.base import BaseCommand

from ....cms.models.cmspost import CmsPost
from ....cms.models.comment import Comment

class Command(BaseCommand):
    help = 'Fetch last comments for posts'

    def handle(self, *args, **options):
        posts = CmsPost.objects.all()

        for post in posts:
            post.last_comment = Comment.objects.filter(post=post, is_deleted=False).order_by('-created_date').first()
            post.save()
