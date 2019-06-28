from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q, Count
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404, render, redirect
from cms.forms.map import MapForm
from cms.utils import is_owner

from cms.models.cmscategory import CmsCategory
from cms.models.map import Map
from django.contrib.auth.models import User


@login_required
@permission_required('cms.map_access', raise_exception=True)
def serve_map_file(request, pk):
    try:
        m = get_object_or_404(Map, pk=pk)

        return HttpResponse(m.file, content_type='image/jpg')
    except KeyError:
        raise Http404("No map found.")



@login_required
@permission_required('cms.map_access', raise_exception=True)
def maps_list(request, tags=None, author=None):
    t = None

    if tags:
        t = tags.split(",")

    if author:
        get_object_or_404(User, username=author)

    query = {
        'tags__name__in': t,
        'author__username': author,
    }

    q = {k: v for k, v in query.items() if v is not None}

    maps_list = Map.objects.filter(Q(**q)).distinct().order_by('-created_date')

    page = request.GET.get('page', 1)

    paginator = Paginator(maps_list, getattr(settings, 'PAGINATION_MAPS_COUNT', 50))
    try:
        maps = paginator.page(page)
    except PageNotAnInteger:
        maps = paginator.page(1)
    except EmptyPage:
        maps = paginator.page(paginator.num_pages)

    categories = CmsCategory.objects.annotate(posts_count=Count('cmspost')).all()
    maps_count = Map.objects.all().count()

    return render(request, 'cms/map_list.html', {
        'maps': maps,
        'tags': t,
        'author': author,
        'categories_list': categories,
        'maps_count': maps_count
    })

@login_required
@permission_required('cms.add_map', raise_exception=True)
def map_new(request):
    if request.method == "POST":
        form = MapForm(request.POST, request.FILES)

        if form.is_valid():
            map = form.save(commit=False)
            map.author = request.user

            map.save()
            form.save_m2m()

            return redirect('maps_list')

    else:
        form = MapForm()

    return render(request, 'cms/map_edit.html', {'form': form})

@login_required
@permission_required('cms.change_map', raise_exception=True)
def map_edit(request, pk):
    map = get_object_or_404(Map, pk=pk)

    if not is_owner(request.user, map):
        raise PermissionDenied()

    if request.method == "POST":
        form = MapForm(request.POST, request.FILES, instance=map)

        if form.is_valid():
            map = form.save(commit=False)
            map.modifed_date = timezone.now()

            map.save()
            form.save_m2m()

            return redirect('maps_list')

    else:
        form = MapForm(instance=map)

    return render(request, 'cms/map_edit.html', {'form': form, 'map': map})

@login_required
@permission_required('cms.delete_map', raise_exception=True)
def map_delete(request, pk):
    map = get_object_or_404(Map, pk=pk)

    if not is_owner(request.user, map):
        raise PermissionDenied()

    map.delete()

    return redirect('maps_list')