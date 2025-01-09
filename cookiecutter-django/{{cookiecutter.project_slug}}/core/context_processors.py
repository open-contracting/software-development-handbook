from django.conf import settings


def from_settings(_request):
    return {
        "fathom": settings.FATHOM,
    }
