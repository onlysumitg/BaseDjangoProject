from functools import partial

from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required

from rest_framework import views, permissions, status
from rest_framework.response import Response
from django_otp import login, devices_for_user
from django_otp.plugins.otp_totp.models import TOTPDevice
from django_otp.util import random_hex
from django_otp.conf import settings

from .utils import is_otp_required
from .models import BooleanSettings

from .forms import OTPTokenForm


@login_required
def ask_for_otp(request):
    user = request.user

    next_url = request.GET.get("next", '/')

    # if not is_safe_url(next_url):
    #     next_url = "/"

    if not is_otp_required(user):
        return redirect(next_url)

    form = None
    if request.method == 'POST':
        form = OTPTokenForm(user=user, data=request.POST)
        if form.is_valid():
            login(request, user.otp_device)
            return redirect(next_url)

    else:
        form = OTPTokenForm(user=user, request=request)
    context = {"form": form}

    return render(request, 'the_user/otp.html', context)


def delete_user_totp_device(user, confirmed = None):
    devices = devices_for_user(user, confirmed=confirmed)
    for device in devices:
        device.delete()


def get_user_totp_device(user, confirmed = None):
    devices = devices_for_user(user, confirmed=confirmed)
    for device in devices:
        if isinstance(device, TOTPDevice):
            return device


def setup_QR_CODE(user):
    key = random_hex(length=35)
    device = get_user_totp_device(user)
    if not device:
        device = user.totpdevice_set.create(confirmed=False,
                                            name="{}:{}".format(settings.OTP_TOTP_ISSUER, user.username), key=key)
    return device


@login_required
def setting_two_factor(request):
    # Profile.objects.all().delete()

    user = request.user
    BooleanSettings.load(user)
    qr_code_url = None
    two_factor_setting = user.booleansettings.get(key=BooleanSettings.AllowedSettings.TWO_FACTOR)

    if request.method == 'POST':
        two_factor = request.POST.get(str(BooleanSettings.AllowedSettings.TWO_FACTOR))
        change2fs = request.POST.get("change2fs")
        if change2fs == "Y":
            message = ""
            if two_factor:
                two_factor_setting.value = True
                device = setup_QR_CODE(user)
                qr_code_url = device.config_url
                message = "Two-factor enabled"
            else:
                two_factor_setting.value = False
                message = "Two-factor disabled"
            two_factor_setting.save()

            if request.create_log_entry:
                request.create_log_entry.send(sender='setting_two_factor', request=request, target=two_factor_setting, message=message)

    if two_factor_setting.value:
        device = setup_QR_CODE(user)
        qr_code_url = device.config_url

    context = {"setting_two_factor": two_factor_setting,
               "qr_code_url": qr_code_url}
    return render(request, 'the_user/setting_two_factor.html', context)


class TOTPVerifyToken(views.APIView):
    """
    Use this endpoint to verify/enable a TOTP device
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format = None):
        token = request.data["token"]
        user = request.user
        device = get_user_totp_device(user)
        if device and device.verify_token(token):
            if not device.confirmed:
                device.confirmed = True
                device.save()

                # auto login user >> on verification
            login(request, device)
            print("request.session[DEVICE_ID_SESSION_KEY]>>>", request.session['otp_device_id'])

            return Response({"verified": True}, status=status.HTTP_200_OK)

        return Response({"verified": False}, status=status.HTTP_200_OK)


class TOTPDeleteDevice(views.APIView):
    """
    Use this endpoint to verify/enable a TOTP device
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format = None):
        reset = request.data["reset"]
        if reset:
            user = request.user
            delete_user_totp_device(user)

        return Response({"done": True}, status=status.HTTP_200_OK)

# class TOTPVerifyView(views.APIView):
#     """
#     Use this endpoint to verify/enable a TOTP device
#     """
#     permission_classes = [permissions.IsAuthenticated]
#
#     def post(self, request, token, format = None):
#         user = request.user
#         device = get_user_totp_device(self, user)
#         # print(device, "xx", device.verify_token(token), "QQ", device and device.verify_token(token))
#         if device and device.verify_token(token):
#             if not device.confirmed:
#                 device.confirmed = True
#                 device.save()
#             return Response(True, status=status.HTTP_200_OK)
#
#         return Response(status=status.HTTP_400_BAD_REQUEST)

# class TOTPCreateView(views.APIView):
#     """
#     Use this endpoint to set up a new TOTP device
#     """
#     permission_classes = [permissions.IsAuthenticated]
#
#     def get(self, request, format = None):
#         user = request.user
#         device = setup_QR_CODE(user)
#         url = device.config_url
#         return Response(url, status=status.HTTP_201_CREATED)
