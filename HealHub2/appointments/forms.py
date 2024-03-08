from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime, timedelta
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

    def clean(self):
        # Custom validation to ensure no overlapping appointments
        cleaned_data = super().clean()
        doctor = cleaned_data.get('doctor')
        date = cleaned_data.get('date')
        time = cleaned_data.get('time')

        if doctor and date and time:
            appointment_start = timezone.make_aware(datetime.combine(date, time))
            appointment_end = appointment_start + timedelta(hours=1)

            overlapping_appointments = Appointment.objects.filter(
                doctor=doctor,
                date=date,
                time__range=(appointment_start.time(), appointment_end.time())
            ).exclude(pk=self.instance.pk if self.instance else None)

            if overlapping_appointments.exists():
                raise ValidationError("There is already an appointment within this time slot for the selected doctor.")

    class Meta:
        model = Appointment
        fields = ['doctor', 'date', 'time', 'description']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }
