from django.apps import AppConfig


class TheUserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'the_user'

    def ready(self):
        # import the_users.signals
        from . import signals