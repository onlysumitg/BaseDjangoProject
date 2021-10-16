from django.urls import re_path, path
from . import views


app_name = 'the_todo'
urlpatterns = [

     path("", views.list_pending_tasks, name="list_pending_tasks"),
     path("completed", views.list_completed_tasks, name="list_completed_tasks"),
     path("create", views.create_task, name="create_task"),
     path("edit/<pk>", views.edit_task, name="edit_task"),


     path("add", views.add_task, name="add_task"),
     path("change_status", views.change_task_status, name="change_status_task"),
    # path("change_status", views.change_task_status, name="change_status_tasks"),

]
