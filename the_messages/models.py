from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from pinax.messages.models import Message


# Create your models here.
class StaredMessage(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name="staredmessage",
                             null=False, blank=False
                             )
    message = models.ForeignKey(Message,
                                on_delete=models.CASCADE,
                                related_name="stared",
                                null=False, blank=False
                                )
    stared = models.BooleanField(verbose_name="Stared", default=False, blank=False, null=False)
