from django.core import serializers
from django.http import JsonResponse

from taggit.models import Tag


def get_simular_tags(request):
    query = request.GET.get('term')
    print(query)
    tags = Tag.objects.filter(name__icontains=query).values('name')

    result = []

    for tag in tags:
        result.append(tag['name'])

    return JsonResponse(list(result), safe=False)