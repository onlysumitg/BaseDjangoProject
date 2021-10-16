from django import forms

from django_otp.forms import OTPAuthenticationFormMixin

from django.conf import settings

from .models import Profile
from django.contrib.auth.models import User
from allauth.account.forms import SignupForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group


# --------------------------------------------------------------------------------
#
# --------------------------------------------------------------------------------
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email", "first_name", "last_name"]


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["mobile_number", 'home_phone_number']


# --------------------------------------------------------------------------------
#
# --------------------------------------------------------------------------------
class OTPTokenForm(OTPAuthenticationFormMixin, forms.Form):
    """
         copy from django_otp.forms.OTPTokenForm

    """
    otp_device = forms.ChoiceField(choices=[], label="Token Type")
    otp_token = forms.CharField(required=True, label="Token", widget=forms.TextInput(attrs={'autocomplete': 'off'}))

    def __init__(self, user, request = None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.user = user
        self.fields['otp_device'].choices = self.device_choices(user)

    def clean(self):
        super().clean()

        self.clean_otp(self.user)

        return self.cleaned_data

    def get_user(self):
        return self.user


# --------------------------------------------------------------------------------
#
# --------------------------------------------------------------------------------

class SignupFormWithGroup(SignupForm):
    AllowedGroups = (

        ("brick_manufacturer", _("Brick Manufacturer")),
        ("brick_supplier", _("Brick Supplier")),
        ("supplier_to_brick_manufacturer", _("Supplier to brick manufacturer")),
        ("enduser", _("None of these")),
    )

    signup_as = forms.ChoiceField(label=_('I am a'), choices=AllowedGroups)

    def save(self, request):
        user = super().save(request)
        group = self.cleaned_data['signup_as']
        new_group, created = Group.objects.get_or_create(name=group)
        user.save()
        new_group.user_set.add(user)
        return user
