from .models import SystemConfig
from django.contrib import admin


def SystemConfigContextProcessor(request):

    app_name = SystemConfig.get("APP_NAME")
    powered_by = SystemConfig.get("POWERED_BY")
    setup_admin()

    if not app_name:
        app_name = "UPDATE APP NAME"  # todo

    if not powered_by:
        powered_by="UPDATE powered by"
    return {"app_name": app_name,"powered_by":powered_by}


def setup_admin():
    app_name = SystemConfig.get(SystemConfig.Config.APP_NAME.name)
    site_header = SystemConfig.get("site_header")
    site_title = SystemConfig.get("site_title")
    index_title = SystemConfig.get("index_title")

    admin.site.site_header = site_header if site_header else app_name
    admin.site.site_title = site_title if site_title else app_name
    admin.site.index_title = index_title if index_title else app_name