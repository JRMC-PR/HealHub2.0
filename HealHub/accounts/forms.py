""""""
from django import forms

class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    phone_number = forms.CharField(max_length=20)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    is_doctor = forms.BooleanField(required=False, widget=forms.CheckboxInput) #Uses a checkbox to determine if the user is a doctor or not
