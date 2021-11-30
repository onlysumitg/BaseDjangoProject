from django.urls import re_path, path
from django.views.generic.base import View
from . import views

app_name = 'the_rules'
urlpatterns = [

    path("", views.RulesList.as_view(), name="rules"),
    path("add", views.RuleCreate.as_view(), name="add"),
    path("<pk>/", views.RuleDetails.as_view(), name="detail"),
    path("<pk>/update", views.RuleUpdate.as_view(), name="update"),
    path("<rule_pk>/condition/", views.RuleConditionsCreate.as_view(), name="create_condition"),
    path("<rule_pk>/condition/<pk>", views.RuleConditionsUpdate.as_view(), name="update_condition"),

    path("x1", views.show_rules, name="show_rules"),

    # re_path(r'^totp/create/$', views.TOTPCreateView.as_view(), name='totp-create'),
    # re_path(r'^totp/login/(?P<token>[0-9]{6})/$', views.TOTPVerifyView.as_view(), name='totp-login'),
]
