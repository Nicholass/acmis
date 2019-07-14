import os

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, Count
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required, permission_required
from hitcount.views import HitCountMixin
from django.core.exceptions import PermissionDenied
from django.core.files.storage import default_storage
from django.views.decorators.csrf import csrf_exempt
from ckeditor_uploader.views import ImageUploadView, get_upload_filename

from PIL import Image

from cms.forms.post import PostForm

from cms.models.cmspost import CmsPost
from cms.models.cmspost_unread import CmsPostUnread
from cms.models.map import Map
from cms.models.cmscategory import CmsCategory
from django.contrib.auth.models import User
from hitcount.models import HitCount
from tracking_analyzer.models import Tracker

from cms.utils import is_owner

def post_list(request, tags=None, category=None, author=None):
    if getattr(settings, 'DEBUG') \
            and request.user.is_authenticated == False \
            and os.getenv('ENV') == 'production':
        return render(request, 'unconstruction.html')

    t = c = None

    if category:
        c = get_object_or_404(CmsCategory, route=category)
        Tracker.objects.create_from_request(request, c)

    if tags:
        t = tags.split(",")

    if author:
        get_object_or_404(User, username=author)

    query = {
        'tags__name__in': t,
        'author__username': author,
        'category': c,
    }

    if not request.user.has_perm('cms.permited_access'):
        query['is_permited'] = False

    q = {k: v for k, v in query.items() if v is not None}

    posts_list = CmsPost.objects.filter(Q(**q)).distinct().order_by('-created_date')

    page = request.GET.get('page', 1)

    paginator = Paginator(posts_list, getattr(settings, 'PAGINATION_POSTS_COUNT', 25))
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    categories = CmsCategory.objects.annotate(posts_count=Count('cmspost')).all()
    maps_count = Map.objects.all().count()

    return render(request, 'cms/post_list.html', {
        'posts': posts,
        'category': c,
        'categories_list': categories,
        'maps_count': maps_count,
        'tags': t,
        'author': author,
    })


def post_detail(request, pk):
    post = get_object_or_404(CmsPost, pk=pk)

    if post.is_permited and not request.user.has_perm('cms.permited_access'):
        raise PermissionDenied()

    hit_count = HitCount.objects.get_for_object(post)
    HitCountMixin.hit_count(request, hit_count)

    if request.user.is_authenticated:
        CmsPostUnread.objects.filter(user=request.user, post=post).delete()

    Tracker.objects.create_from_request(request, post)

    return render(request, 'cms/post_detail.html', {'post': post})


@login_required
@permission_required('cms.add_cmspost', raise_exception=True)
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user

            post.save()
            form.save_m2m()

            return redirect('post_detail', pk=post.pk)

    else:
        form = PostForm()

    return render(request, 'cms/post_edit.html', {'form': form})


@login_required
@permission_required('cms.change_cmspost', raise_exception=True)
def post_edit(request, pk):
    post = get_object_or_404(CmsPost, pk=pk)

    if not is_owner(request.user, post):
        raise PermissionDenied()

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)

        if form.is_valid():
            post = form.save(commit=False)
            post.modifed_date = timezone.now()

            post.save()
            form.save_m2m()

            return redirect('post_detail', pk=post.pk)

    else:
        form = PostForm(instance=post)

    return render(request, 'cms/post_edit.html', {'form': form, 'post': post})


@login_required
@permission_required('cms.delete_cmspost', raise_exception=True)
def post_delete(request, pk):
    post = get_object_or_404(CmsPost, pk=pk)

    if not is_owner(request.user, post):
        raise PermissionDenied()

    post.delete()

    return redirect('category_list', category=post.category.route)

def calculate_size(img):
    IMAGE_SIZE = getattr(settings, 'IMAGES_SIZE', (1024, 768))

    img_ratio = img.size[0] / float(img.size[1])
    ratio = IMAGE_SIZE[0] / float(IMAGE_SIZE[1])

    if ratio > img_ratio:
        if img.size[1] > IMAGE_SIZE[0]:
            return (IMAGE_SIZE[0], int(IMAGE_SIZE[0] * img.size[1] / img.size[0]))
    else:
        if img.size[0] > IMAGE_SIZE[1]:
            return (int(IMAGE_SIZE[1] * img.size[0] / img.size[1]), IMAGE_SIZE[1])

    return img.size


class ImageUploadViewResize(ImageUploadView):
    def __init__(self, *args):
        super().__init__(*args)

    @staticmethod
    def _save_file(request, uploaded_file):
        filename = get_upload_filename(uploaded_file.name, request.user)

        img_name, img_format = os.path.splitext(filename)
        IMAGE_QUALITY = getattr(settings, "IMAGE_QUALITY", 60)
        MEDIA_ROOT = getattr(settings, "MEDIA_ROOT")

        saved_path = default_storage.save(filename, uploaded_file)

        if(str(img_format).lower() == ".png"):

            img = Image.open(uploaded_file)
            img = img.resize(calculate_size(img), Image.ANTIALIAS)

            img.save(os.path.join(MEDIA_ROOT, saved_path), quality=IMAGE_QUALITY, optimize=True)

        elif(str(img_format).lower() == ".jpg" or str(img_format).lower() == ".jpeg"):

            img = Image.open(uploaded_file)
            img = img.resize(calculate_size(img), Image.ANTIALIAS)

            img.save(os.path.join(MEDIA_ROOT, saved_path), quality=IMAGE_QUALITY, optimize=True)

        return saved_path


upload = csrf_exempt(ImageUploadViewResize.as_view())