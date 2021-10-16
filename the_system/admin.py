from django.contrib import admin

from .models import SystemConfig
# Register your models here.

@admin.register(SystemConfig)
class SystemConfigAdmin(admin.ModelAdmin):
    list_display = ("config", "value",)
    search_fields = ("config",)