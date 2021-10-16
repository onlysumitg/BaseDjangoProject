from django.urls import re_path, path
from . import views

app_name = 'the_system'
urlpatterns = [

    path("", views.landing_page, name="landing_page"),
    path("toggletheme", views.ToggleTheme.as_view(), name="toggle_theme"),

    # re_path(r'^totp/create/$', views.TOTPCreateView.as_view(), name='totp-create'),
    # re_path(r'^totp/login/(?P<token>[0-9]{6})/$', views.TOTPVerifyView.as_view(), name='totp-login'),
]
