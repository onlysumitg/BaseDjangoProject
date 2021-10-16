from django.urls import re_path, path
from . import views

from .views import list_sent_message,ToggleStared,list_started_message

app_name = 'the_messages'
urlpatterns = [

    path("sentmessages", list_sent_message, name="sent_messages"),
    path("staredmessages", list_started_message, name="stared_messages"),
    path("togglestar", ToggleStared.as_view(), name="messages_toggle_start"),


    # re_path(r'^totp/create/$', views.TOTPCreateView.as_view(), name='totp-create'),
    # re_path(r'^totp/login/(?P<token>[0-9]{6})/$', views.TOTPVerifyView.as_view(), name='totp-login'),
]
