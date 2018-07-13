from django.conf import settings


def export_settings(request):
    # return any necessary values
    return {
        'AVATAR_MAX_WIDTH': settings.AVATAR_MAX_WIDTH,
        'AVATAR_MAX_HEIGHT': settings.AVATAR_MAX_HEIGHT,
        'AVATAR_DEFAULT': settings.AVATAR_DEFAULT,
        'AVATAR_DIMENSIONS': settings.AVATAR_DIMENSIONS,
    }