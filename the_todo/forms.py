from django import forms

from django_otp.forms import OTPAuthenticationFormMixin

from django.conf import settings

from .models import Todo
from django.contrib.auth.models import User


# --------------------------------------------------------------------------------
#
# --------------------------------------------------------------------------------
class TodoFormEdit(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ["task","completed",
                  ]



# --------------------------------------------------------------------------------
#
# --------------------------------------------------------------------------------
class TodoFormCreate(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ["task","completed" ,
                  ]


