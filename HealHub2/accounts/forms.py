from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
  """
  A form for creating new users. It includes all the required fields, plus a repeated password.
  """
  email = forms.EmailField()
  Doctor = forms.BooleanField(required=False, widget=forms.CheckboxInput)

  class Meta:
    model = User
    fields = ["username", "email", "password1", "password2", "first_name", "last_name", "Doctor"]
