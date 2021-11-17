from django.conf import settings


def from_settings(request):
    return {
        "fathom": settings.FATHOM,
    }
