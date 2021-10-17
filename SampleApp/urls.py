import django.conf.urls
from django.contrib import admin
from django.urls import path, include

#import views
from SampleApp import views_function_based
#import views_class_based


app_name = 'sampleapp'

urlpatterns = [
    path('functionview1', views_function_based.function_based_view_1, name='function_view_1'),


]
