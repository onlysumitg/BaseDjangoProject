from django_otp import user_has_device
from .models import BooleanSettings


def is_otp_required(user):
    two_factor_enabled = user.booleansettings.get(key=BooleanSettings.AllowedSettings.TWO_FACTOR)
    if not two_factor_enabled.value:
        return False

    if not user_has_device(user):
        return False

    if user.is_verified():
        return False

    return True


def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()