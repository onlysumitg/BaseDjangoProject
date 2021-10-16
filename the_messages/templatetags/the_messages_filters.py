from django import template

register = template.Library()

from ..models import StaredMessage


@register.filter(name='is_stared')
def is_stared(message, request):
    user = request.user
    started_count = StaredMessage.objects.filter(user=user).filter(message=message, stared = True).count()

    if started_count > 0:
        return True
    else:
        return False
