from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Appointment(models.Model):
    patient = models.ForeignKey(User, related_name='appointments_as_patient', on_delete=models.CASCADE)
    doctor = models.ForeignKey(User, related_name='appointments_as_doctor', on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    description = models.TextField()
    phone = models.CharField(max_length=15, default='7877512266')  # Phone field with a default value

    def clean(self):
        # Ensure the referenced doctor user has a profile marked as a doctor
        if not self.doctor.profile.doctor:
            raise ValidationError("The selected doctor is not marked as a doctor in their profile.")

    def __str__(self):
        return f"Appointment on {self.date} at {self.time} with Dr. {self.doctor.profile.specialty} and patient {self.patient.username}\
            (phone: {self.phone})"

    class Meta:
        # Optional: enforce unique appointments for a doctor at a given time
        unique_together = ('doctor', 'date', 'time')

