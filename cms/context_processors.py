from django.conf import settings


def export_settings(request):
    # return any necessary values
    return {
        'AVATAR_WIDTH': settings.AVATAR_WIDTH,
        'AVATAR_HEIGHT': settings.AVATAR_HEIGHT,
        'AVATAR_DEFAULT': settings.AVATAR_DEFAULT,
    }