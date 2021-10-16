from django.contrib.auth.models import User
from django.db.models.signals import post_save
from allauth.account.signals import user_logged_in, password_changed, password_reset, email_confirmed, \
    email_confirmation_sent, email_changed
from django.dispatch import receiver
from django.utils.translation import gettext, gettext_lazy as _

from dataclasses import dataclass
from typing import Any

from django.db.models import Model

from .models import UserActivity

from .signals import create_log_entry

'''
https://docs.djangoproject.com/en/dev/ref/request-response/#django.http.HttpRequest.META

CONTENT_LENGTH – The length of the request body (as a string).
CONTENT_TYPE – The MIME type of the request body.
HTTP_ACCEPT – Acceptable content types for the response.
HTTP_ACCEPT_ENCODING – Acceptable encodings for the response.
HTTP_ACCEPT_LANGUAGE – Acceptable languages for the response.
HTTP_HOST – The HTTP Host header sent by the client.
HTTP_REFERER – The referring page, if any.
HTTP_USER_AGENT – The client’s user-agent string.
QUERY_STRING – The query string, as a single (unparsed) string.
REMOTE_ADDR – The IP address of the client.  <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
REMOTE_HOST – The hostname of the client.      <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
REMOTE_USER – The user authenticated by the Web server, if any.
REQUEST_METHOD – A string such as "GET" or "POST". <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
SERVER_NAME – The hostname of the server.
SERVER_PORT – The port of the server (as a string).

'''


@receiver(create_log_entry)
def create_log_entry_logger(request: Any = None, user_to_use: Model = None, target: Model = None, message: str = '',
                            **kwargs):
    if request:

        # request = log_entry_data.request
        # print("request.META['CONTENT_LENGTH']", request.META['CONTENT_LENGTH'])
        # print("request.META['CONTENT_TYPE']", request.META['CONTENT_TYPE'])
        # print("request.META['HTTP_ACCEPT']", request.META['HTTP_ACCEPT'])
        # print("request.META['HTTP_ACCEPT_ENCODING']", request.META['HTTP_ACCEPT_ENCODING'])
        # print("request.META['HTTP_ACCEPT_LANGUAGE']", request.META['HTTP_ACCEPT_LANGUAGE'])
        # print("request.META['HTTP_HOST']", request.META['HTTP_HOST'])
        # print("request.META['HTTP_REFERER']", request.META['HTTP_REFERER'])
        # print("request.META['HTTP_USER_AGENT']", request.META['HTTP_USER_AGENT'])
        # print("request.META['QUERY_STRING']", request.META['QUERY_STRING'])
        # print("request.META['REMOTE_ADDR']", request.META['REMOTE_ADDR'])
        # print("request.META['REMOTE_HOST']", request.META['REMOTE_HOST'])
        # print("request.META['REQUEST_METHOD']", request.META['REQUEST_METHOD'])
        # print("request.META['SERVER_NAME']", request.META['SERVER_NAME'])
        # print("request.META['SERVER_PORT']", request.META['SERVER_PORT'])

        user = request.user
        ip_address = request.META['REMOTE_ADDR']
        user_agent = request.META['HTTP_USER_AGENT']
        path = request.META['HTTP_REFERER']
    else:
        user = user_to_use

    # if create_log_entry.target:
    #     content_type = ContentType.objects.get_for_model(log_entry_data.target)
    #     object_id = log_entry_data.target.id

    if message:
        user_activity = UserActivity(user=user,
                                     target=target,
                                     change_message=_(message),
                                     ip_address=ip_address,
                                     user_agent=user_agent,
                                     path=path
                                     )

        user_activity.save()


'''
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE

def log_action(self, user_id, content_type_id, object_id, object_repr, action_flag, change_message=''):
    
LogEntry.objects.log_action(
            user_id=request.user.id,
            content_type_id=ContentType.objects.get_for_model(model_object).pk,
            object_id=object.id,
            object_repr=unicode(object.title),
            action_flag=ADDITION if create else CHANGE)

'''


# -------------------------------------------------
#  capture other signals
# -------------------------------------------------


@receiver(post_save, sender=User)
def on_save_user_profile(sender, instance, **kwargs):
    pass


@receiver(user_logged_in)
def login_logger(request, user, **kwargs):
    print("{} logged in with {}".format(user.email, request))
    create_log_entry_logger(request=request, message="Logged in")


@receiver(password_changed)
def password_changed(request, user, **kwargs):
    create_log_entry_logger(request=request, message="Password Changed")


@receiver(password_reset)
def password_reset(request, user, **kwargs):
    pass


@receiver(email_confirmed)
def email_confirmed(request, email_address, **kwargs):
    create_log_entry_logger(request=request, message="Email Confirmed")


@receiver(email_confirmation_sent)
def email_confirmation_sent(request, confirmation,signup, **kwargs):
    create_log_entry_logger(request=request, message="Email Confirmation Sent")


@receiver(email_changed)
def email_changed(request, user,from_email_address,to_email_address, **kwargs):
    create_log_entry_logger(request=request, message="Email Changed")
