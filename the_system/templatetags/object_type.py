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