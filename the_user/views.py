from django.shortcuts import render

from .forms import UserForm, UserProfileForm
from .models import BooleanSettings
# Create your views here.
from django.contrib.auth.decorators import login_required

from the_user.decorators import otp_required


@login_required
@otp_required
def setting(request):
    # Profile.objects.all().delete()
    user = request.user
    user_form = UserForm()
    profile_form = UserProfileForm()

    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user_data = user_form.cleaned_data
            profile_data = profile_form.cleaned_data
           # user.username = user_data['username']
            user.email = user_data['email']
            user.first_name = user_data['first_name']
            user.last_name = user_data['last_name']
            user.profile.mobile_number = profile_data['mobile_number']
            user.profile.home_phone_number = profile_data['home_phone_number']
            user.save()
            user.profile.save()

            # user = user_form.save()
            # profile = profile_form.save(commit=False)
            # profile.user = user
            # profile.save()
    else:
        # user_form.fields["username"].initial = user.username
        user_form.fields["email"].initial = user.email
        user_form.fields["first_name"].initial = user.first_name
        user_form.fields["last_name"].initial = user.last_name
        profile_form.fields["mobile_number"].initial = user.profile.mobile_number
        profile_form.fields["home_phone_number"].initial = user.profile.home_phone_number

    context = {"user_form": user_form, "profile_form": profile_form}
    return render(request, 'the_user/settings.html', context)

# -------------------------------------------------


#
# @login_required
# def verify(request):
#     form_cls = partial(OTPTokenForm, request.user)
#
#     return LoginView.as_view(request, template_name='account/otp.html', authentication_form=form_cls)
