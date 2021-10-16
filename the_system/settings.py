from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


def get_page_size():
    page_size = 25
    try:
        page_size = int(settings.PAGE_SIZE)
    except AttributeError:
        page_size = 0
    except(TypeError, ValueError):
        page_size = 0

    print("page_size", page_size, int(settings.PAGE_SIZE))

    if page_size <= 0:
        page_size = 25

    return page_size
