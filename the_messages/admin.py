from django.contrib import admin

# Register your models here.
from .models import StaredMessage

@admin.register(StaredMessage)
class StaredMessageAdmin(admin.ModelAdmin):
    list_display = ("user", "message","stared")
