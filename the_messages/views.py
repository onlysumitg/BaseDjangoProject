from django.shortcuts import render
from rest_framework import views, permissions, status
from rest_framework.response import Response
# Create your views here.
from the_system.utils import get_paginator

from pinax.messages.models import Message
from .models import StaredMessage

from django.contrib.auth.decorators import login_required

from the_user.decorators import otp_required


@login_required
@otp_required
def list_sent_message(request):
    user = request.user

    if request.search_value:
        messages = Message.objects.filter(sender=user).filter(content__icontains=request.search_value)


    else:
        messages = Message.objects.filter(sender=user)

    page_number, sent_messages = get_paginator(request, messages)
    context = {"sent_messages": sent_messages, "page": page_number}

    return render(request, 'the_messages/sent_message_list.html', context)

@login_required
@otp_required
def list_started_message(request):
    user = request.user

    if request.search_value:
        stared_messages = StaredMessage.objects.filter(user=user).filter(content__icontains=request.search_value)


    else:
        stared_messages = StaredMessage.objects.filter(user=user).values("message")

    messages = []
    for stared in stared_messages:
        messages.append(Message.objects.get(pk=stared["message"]))

    page_number, stared_messages = get_paginator(request, messages)
    context = {"stared_messages": stared_messages, "page": page_number}

    return render(request, 'the_messages/stared_message_list.html', context)


class ToggleStared(views.APIView):
    """
    Use this endpoint to verify/enable a TOTP device
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format = None):
        messageid = request.data["messageid"]
        success = False
        if messageid:

            message = Message.objects.get(pk=messageid);

            # todo optimize request.user in message.thread.users.all()
            if message and (request.user in message.thread.users.all()):
                try:
                    stared_message = StaredMessage.objects.get(user=request.user, message=message)
                except Exception:
                    stared_message = None

                if stared_message:
                    stared_message.delete()
                else:
                    stared_message = StaredMessage()
                    stared_message.user = request.user
                    stared_message.message = message
                    stared_message.stared = True
                    stared_message.save()
                success = True

        return Response({"done": success}, status=status.HTTP_200_OK)
