from django.shortcuts import render
from rest_framework.decorators import api_view, throttle_classes
from rest_framework import views, permissions, status
from django.shortcuts import render, get_object_or_404, redirect

from rest_framework.response import Response
from .forms import TodoFormCreate, TodoFormEdit
from .models import Todo
# Create your views here.

from django.contrib.auth.decorators import login_required

from the_user.decorators import otp_required
from the_system.utils import get_paginator


# ------------------------------------------------------------------
#
# ------------------------------------------------------------------

@login_required
@otp_required
def list_completed_tasks(request):
    if request.search_value:
        user_tasks = Todo.objects.filter(user=request.user).filter(
            task__icontains=request.search_value.lower()).filter(completed=True)
    else:
        user_tasks = Todo.objects.filter(user=request.user).filter(completed=True)

    page_number, tasks = get_paginator(request, user_tasks)

    context = {"tasks": tasks, "page": page_number}
    return render(request, 'the_todo/completed_task_list.html', context)


# ------------------------------------------------------------------
#
# ------------------------------------------------------------------

@login_required
@otp_required
def list_pending_tasks(request):
    if request.search_value:
        user_tasks = Todo.objects.filter(user=request.user).filter(
            task__icontains=request.search_value.lower()).filter(completed=False)
    else:
        user_tasks = Todo.objects.filter(user=request.user).filter(completed=False)

    page_number, tasks = get_paginator(request, user_tasks)

    context = {"tasks": tasks, "page": page_number}
    return render(request, 'the_todo/task_list.html', context)


# ------------------------------------------------------------------
#
# ------------------------------------------------------------------
@login_required
@otp_required
def create_task(request):
    create_form = TodoFormCreate()
    next = request.GET.get('next', '/')

    if request.method == "POST":
        create_form = TodoFormCreate(data=request.POST)
        if create_form.is_valid():
            create_form.instance.user = request.user
            create_form.save()
            return redirect(next)
    context = {"form": create_form,"action":"Create" }
    return render(request, 'the_todo/task_create.html', context)


# ------------------------------------------------------------------
#
# ------------------------------------------------------------------
@login_required
@otp_required
def edit_task(request, pk):
    todo = get_object_or_404(Todo, pk=pk, user=request.user)
    edit_form = TodoFormEdit(request.POST or None, instance=todo)
    next = request.GET.get('next', '/')



    if request.method == "POST":
        edit_form = TodoFormEdit(data=request.POST)
        if edit_form.is_valid():


            task_data = edit_form.cleaned_data
            todo.task = task_data["task"]
            todo.completed = task_data["completed"]
            todo.save()

            return redirect(next)

    context = {"form": edit_form, "action":"Edit", }
    return render(request, 'the_todo/task_create.html', context)




# ------------------------------------------------------------------
#
# ------------------------------------------------------------------
@api_view(['POST', ])
@login_required
@otp_required
def add_task(request):
    if request.method == 'POST':
        task = request.data["task"]
        if task:
            todo = Todo()

            todo.task = task
            todo.user = request.user
            todo.completed = False
            todo.save()
        else:
            return Response({"done": False}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"done": True}, status=status.HTTP_200_OK)


# ------------------------------------------------------------------
#
# ------------------------------------------------------------------
@api_view(['POST', ])
@login_required
@otp_required
def change_task_status(request):
    if request.method == 'POST':
        task_id = request.data["taskid"]

        try:
            todo = Todo.objects.get(pk=task_id, user=request.user)
        except Exception:
            todo = None

        if not todo:
            return Response({"done": False}, status=status.HTTP_400_BAD_REQUEST)
        else:
            todo.completed = not todo.completed
            todo.save()
    return Response({"done": True}, status=status.HTTP_200_OK)
