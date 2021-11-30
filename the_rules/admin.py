from django.contrib import admin
from .models import Rule, RuleConditions
# Register your models here.
@admin.register(Rule)
class RuleStorageAdmin(admin.ModelAdmin):
    field = '__All__'


@admin.register(RuleConditions)
class RuleConditionsAdmin(admin.ModelAdmin):
    field = '__All__'