from django.db import models

# Create your models here.


class SampleModel(models.Model):
    """
      null -> if db can have null value or not
      blank -> if user is allowed to provide a blank value

      if user provide a blank value does not mean db can also handle that

    """
    first_name = models.CharField(max_length=100, null=False, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        verbose_name= "My Sample Model 1"