# https://docs.djangoproject.com/en/3.1/howto/custom-template-tags/#writing-custom-template-tags

from django import template
from django.conf import settings
import json

# this is required
register = template.Library()


@register.filter
def classname(obj):
    return obj.__class__.__name__


@register.filter
def to_json(obj):
    return json.dumps(obj)

@register.filter(name='get_current_url_without_lang')
def get_current_url_without_lang(request, current_language):
    get_full_path = request.get_full_path()
    current_language_string = f"/{current_language}"
    print("current_language_string>>>>", current_language_string,get_full_path )
    if get_full_path.startswith(current_language_string):
        get_full_path = get_full_path.replace(current_language_string, '', 1)
        print("get_full_path>>>>", get_full_path)

    return get_full_path