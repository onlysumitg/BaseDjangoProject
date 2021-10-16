from django.urls import re_path, path
from . import views

from .views_otp import ask_for_otp,setting_two_factor,TOTPVerifyToken,TOTPDeleteDevice

app_name = 'the_user'
urlpatterns = [


    path("settings/", views.setting, name="settings"),
    path("settings/twofactor/", setting_two_factor, name="setting_two_factor"),
    path("twofactor/", ask_for_otp, name="ask_for_otp"),
    path("verify2ft/", TOTPVerifyToken.as_view(), name="setting_two_factor_verification"),
    path("reset2ft/", TOTPDeleteDevice.as_view(), name="setting_two_factor_reset"),


    # re_path(r'^totp/create/$', views.TOTPCreateView.as_view(), name='totp-create'),
    # re_path(r'^totp/login/(?P<token>[0-9]{6})/$', views.TOTPVerifyView.as_view(), name='totp-login'),
]


