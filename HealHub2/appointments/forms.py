from django import forms
from django.contrib.auth.models import User
from django.db.models import F, Value as V
from django.db.models.functions import Concat
from .models import Appointment

class AppointmentForm(forms.ModelForm):
    doctor = forms.ModelChoiceField(
        queryset=User.objects.none(),  # Initially empty, set in __init__
        label="Doctor",
        required=True,
    )

    def __init__(self, *args, **kwargs):
        super(AppointmentForm, self).__init__(*args, **kwargs)
        # Filter users marked as doctors and set queryset for the doctor field
        self.fields['doctor'].queryset = User.objects.filter(profile__doctor=True)

        # Optionally, customize the label from within the __init__ if needed
        self.fields['doctor'].label_from_instance = self.label_from_instance

    def label_from_instance(self, obj):
        # Return a string of the format: "Firstname Lastname - Specialty"
        return f"{obj.get_full_name()} - {obj.profile.specialty}"

    class Meta:
        model = Appointment
        fields = ['doctor', 'date', 'time', 'description', 'phone']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }

