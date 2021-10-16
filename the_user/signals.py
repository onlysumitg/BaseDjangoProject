from django.contrib.auth.models import User
from django.db.models.signals import post_save
from allauth.account.signals import user_logged_in, password_changed, password_reset, email_confirmed, \
    email_confirmation_sent, email_changed
from .models import Profile, BooleanSettings
from django.dispatch import receiver


def create_profile(user):
    if hasattr(user, 'profile'):
        pass
    else:
        Profile.objects.create(user=user)


@receiver(post_save, sender=User)
def on_save_user_profile(sender, instance, **kwargs):
    # create user profile
    user = instance
    create_profile(user)

    BooleanSettings.load(user)


@receiver(user_logged_in)
def login_logger(request, user, **kwargs):
    print("{} logged in with {}".format(user.email, request))


# @receiver(password_changed)
# def password_changed(request, user, **kwargs):
#     pass
#
#
# @receiver(password_reset)
# def password_reset(request, user, **kwargs):
#     pass
#
#
# @receiver(email_confirmed)
# def email_confirmed(request, user, **kwargs):
#     pass
#
#
# @receiver(email_confirmation_sent)
# def email_confirmation_sent(request, user, **kwargs):
#     pass
#
#
# @receiver(email_changed)
# def email_changed(request, user, **kwargs):
#     pass
