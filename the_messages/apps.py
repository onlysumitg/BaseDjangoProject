# this app is extension to pinax messages
# https://github.com/pinax/pinax-messages#templates
# https://templates.pinaxproject.com/messages/threads/1/delete/

from django.apps import AppConfig


class TheMessagesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'the_messages'
