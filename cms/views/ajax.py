from django.core import serializers
from django.http import JsonResponse

from taggit.models import Tag


def get_simular_tags(request, part=None):
    tags = Tag.objects.filter(name__icontains=part).values('name')

    return JsonResponse(list(tags), safe=False)