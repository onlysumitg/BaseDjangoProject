from django.apps import AppConfig


class TheSystemConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'the_system'

    def ready(self):
        print("Starting the server >>>>>>> ")

        # from .models import SystemConfig
        # from django.contrib import admin
        # app_name = SystemConfig.get(SystemConfig.Config.APP_NAME.name)
        # site_header = SystemConfig.get("site_header")
        # site_title = SystemConfig.get("site_title")
        # index_title = SystemConfig.get("index_title")
        #
        # admin.site.site_header = site_header if site_header else app_name
        # admin.site.site_title = site_title if site_title else app_name
        # admin.site.index_title = index_title if index_title else app_name
