from django import forms
from django.contrib.auth.models import User
from .models import Appointment

class AppointmentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AppointmentForm, self).__init__(*args, **kwargs)
        # Filter users marked as doctors
        self.fields['doctor'].queryset = User.objects.filter(profile__doctor=True)

    class Meta:
        model = Appointment
        fields = ['patient', 'doctor', 'date', 'time', 'description']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }
