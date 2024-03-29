from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Appointment
from accounts.models import Profile

class AppointmentForm(forms.ModelForm):
    """
    A form for creating and editing appointments.
    The form fields are adjusted based on the role of the user (doctor or patient).
    """

    # These fields are declared to ensure they can be conditionally included
    # based on the role of the user creating the form.
    patient = forms.ModelChoiceField(
        queryset=User.objects.none(),  # This will be overridden in __init__
        label="Patient",
        required=False,  # Requirement is conditionally applied in __init__
    )

    doctor = forms.ModelChoiceField(
        queryset=User.objects.none(),  # This will be overridden in __init__
        label="Doctor",
        required=False,  # Requirement is conditionally applied in __init__
    )

    def __init__(self, *args, **kwargs):
        """
        Initialize the form.
        Adjust the form fields based on whether the user is a doctor or a patient.
        """
        user = kwargs.pop('user', None)  # Extract the user before calling super
        super().__init__(*args, **kwargs)

        # Adjust the form fields based on whether the user is a doctor.
        if user is not None and hasattr(user, 'profile'):
            if user.profile.doctor is True:
                self.fields['patient'].queryset = User.objects.filter(profile__doctor=False)
                self.fields['patient'].required = True
                self.fields['doctor'].initial = user
                self.fields['doctor'].widget = forms.HiddenInput()
                self.fields['doctor'].queryset = User.objects.filter(id=user.id)  # Only the user as doctor
            elif user.profile.doctor is False:
                self.fields['doctor'].queryset = User.objects.filter(profile__doctor=True)
                self.fields['doctor'].required = True
                self.fields['patient'].initial = user
                self.fields['patient'].widget = forms.HiddenInput()
                self.fields['patient'].queryset = User.objects.filter(id=user.id)  # Only the user as patient

            # Custom label to include specialty for doctors
            self.fields['doctor'].label_from_instance = lambda obj: f"{obj.get_full_name()} - {obj.profile.specialty}" if obj.profile.doctor else obj.get_full_name()

    def clean_date(self):
        """
        Validate the date.
        Ensure that the appointment date is not in the past.
        """
        date = self.cleaned_data['date']
        if date < timezone.localdate():
            raise ValidationError("Appointments cannot be set in the past.")
        return date

    def clean_time(self):
        """
        Validate the time.
        Ensure that the appointment time is on the hour (i.e., minutes and seconds are 0).
        """
        time = self.cleaned_data['time']
        if time.minute != 0 or time.second != 0:
            raise ValidationError("Only the hour can be selected for appointments.")
        return time.replace(minute=0, second=0, microsecond=0)

    def clean(self):
        """
        Validate the form.
        Ensure the appointment does not overlap with existing appointments.
        """
        cleaned_data = super().clean()
        doctor = cleaned_data.get('doctor')
        date = cleaned_data.get('date')
        time = cleaned_data.get('time')

        # Ensure the appointment does not overlap with existing appointments
        if doctor and date and time:
            appointment_start = timezone.make_aware(datetime.combine(date, time))
            appointment_end = appointment_start + timedelta(hours=1)
            overlapping_appointments = Appointment.objects.filter(
                doctor=doctor,
                date=date,
                time__gte=appointment_start.time(),
                time__lt=appointment_end.time()
            ).exclude(pk=self.instance.pk if self.instance else None)

            if overlapping_appointments.exists():
                self.add_error('time', "There is already an appointment within this time slot for the selected doctor.")

    class Meta:
        """
        Meta class for the AppointmentForm.
        Specifies the model, fields, and widgets to be used by the form.
        """
        model = Appointment
        fields = ['doctor', 'patient', 'date', 'time', 'description']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }
