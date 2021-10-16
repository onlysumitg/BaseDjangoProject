from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.

class SystemConfig(models.Model):
    class Config(models.TextChoices):
        APP_NAME = 'APP_NAME', _('APPLICATION NAME')
        SITE_HEADER = 'SITE_HEADER', _('ADMIN SITE HEADER')
        SITE_TITLE = 'SITE_TITLE', _('ADMIN SITE TITLE')
        INDEX_TITLE = 'INDEX_TITLE', _('ADMIN SITE INDEX TITLE')
        POWERED_BY = 'POWERED_BY', _('POWERED BY WEBSITE')

    config = models.CharField(max_length=25, primary_key=True, verbose_name="Configuration Name",
                              choices=Config.choices)
    value = models.CharField(max_length=100, verbose_name="Value")

    class Meta:
        verbose_name = "System Configuration"

    def __str__(self):
        return self.config

    @staticmethod
    def get(config):
        config = str(config).upper()
        try:
            config_object = SystemConfig.objects.get(config=config)
        except Exception as e:
            return ""

        if config_object:
            return config_object.value

        return ""
