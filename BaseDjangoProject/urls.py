"""BaseDjangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import os
import django.conf.urls
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse, HttpResponseForbidden,HttpResponseNotFound, Http404
from django.conf import settings

from django.conf.urls.i18n import i18n_patterns

#@login_required
def media_access(request, path):

    user = request.user
    if user.is_authenticated:
        # Split the elements of the path
        path2, file_name = os.path.split(path)

        response = HttpResponse()
        response["Content-Disposition"] = "attachment; filename=" + file_name

        return response
    else:
        #return HttpResponseForbidden('Not authorized!')
        #return HttpResponseNotFound('<h1>Page not found</h1>')
        raise Http404("Page not Found")


urlpatterns = i18n_patterns(

    #path('', views.home),  #home page >  the_users> views> home() [login required]> ... /templates/the_users/index.html
#    path('', include('the_users.urls')),  #home page >  the_users> views> home() [login required]> ... /templates/the_users/index.html
    path('', include('the_system.urls')),

    path('dont/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path("todo/", include('the_todo.urls')),
    django.conf.urls.url(r'^media/(?P<path>.*)', media_access, name='media'),
    path('rosetta/', include('rosetta.urls')),
    path("messages/", include("pinax.messages.urls", namespace="pinax_messages")),
    path("messagesext/", include('the_messages.urls')),

    path('user/', include('the_user.urls')),

    path('activity/', include('the_activity.urls')),

    path('i18n/', include('django.conf.urls.i18n'))


) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

