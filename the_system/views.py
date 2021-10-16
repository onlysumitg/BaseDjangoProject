from django.shortcuts import render
from rest_framework import views, permissions, status
from rest_framework.response import Response

from django.contrib.auth.decorators import login_required
from the_user.decorators import otp_required

@login_required
@otp_required
def landing_page(request):
    # todo: where to land user on login
    return render(request, 'the_system/landing_page.html', {})

class ToggleTheme(views.APIView):
    """
    Use this endpoint to verify/enable a TOTP device
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format = None):
        theme = request.data["theme"]
        if theme:
            request.session["uitheme"] = theme

        return Response({"done": True}, status=status.HTTP_200_OK)
