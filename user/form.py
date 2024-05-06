from .models import *
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ['nid', 'ph_no', 'role', 'status', 'address']


class UserForm(UserCreationForm):
    first_name = forms.CharField(max_length=255, required=True)
    last_name = forms.CharField(max_length=255, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = True  # Set is_staff to True
        user.is_active = False  # Set is_active to False
        if commit:
            user.save()
        return user

class VerifyOtpForm(forms.ModelForm):
    # is_staff = forms.BooleanField(initial=True, widget=forms.HiddenInput())
    class Meta:
        model = VerifyOtp
        fields = ['otp']