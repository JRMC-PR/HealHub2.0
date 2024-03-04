""""""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import Accounts

class SignupForm(forms.Form, UserCreationForm):
    USERNAME_FIELD = forms.CharField(max_length=40)
    email = forms.EmailField()
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    phone_number = forms.CharField(max_length=20)
    is_doctor = forms.BooleanField(required=False, widget=forms.CheckboxInput) #Uses a checkbox to determine if the user is a doctor or not

    class Meta:
        model = Accounts
        fields = ['USERNAME_FIELD', 'first_name', 'last_name', 'phone_number', 'email', 'password1', 'password2', 'is_doctor']

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
