from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

class Appointment(models.Model):
    """
    This model represents an appointment in the system.
    An appointment has a patient, a doctor, a date, a time, a description, and a phone number.
    """
    # Foreign key relationships to the User model for patient and doctor
    patient = models.ForeignKey(User, related_name='appointments_as_patient', on_delete=models.CASCADE)
    doctor = models.ForeignKey(User, related_name='appointments_as_doctor', on_delete=models.CASCADE)

    # Date and time of the appointment
    date = models.DateField()
    time = models.TimeField()

    # Description of the appointment
    description = models.TextField()

    # Phone number for the appointment with a default value
    phone = models.CharField(max_length=15, default='7877512266')

    def clean(self):
        """
        Custom validation for the Appointment model.
        Ensures the referenced doctor user has a profile marked as a doctor.
        """
        if not self.doctor.profile.doctor:
            raise ValidationError("The selected doctor is not marked as a doctor in their profile.")

    def __str__(self):
        """
        String representation of the Appointment model.
        Includes the date, time, doctor's specialty, patient's username, and phone number.
        """
        return f"Appointment on {self.date} at {self.time} with Dr. {self.doctor.profile.specialty} and patient {self.patient.username}\
            (phone: {self.phone})"

    class Meta:
        """
        Meta class for the Appointment model.
        Enforces unique appointments for a doctor at a given time.
        """
        unique_together = ('doctor', 'date', 'time')
