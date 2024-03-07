from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
  """
  A form for creating new users. It includes all the required fields, plus a repeated password.
  """
  email = forms.EmailField()
  is_staff = forms.BooleanField(required=False, widget=forms.CheckboxInput, help_text="Check this box if you are a doctor")

  class Meta:
    model = User
    fields = ["username", "email", "password1", "password2", "first_name", "last_name", "is_staff"]
