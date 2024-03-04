# """"""
# from django.db import models

# # Create your models here.

# from django.db import models
# from .models import Accounts  # Replace with your actual accounts app name

# class Appointment(models.Model):
#     doctor = models.ForeignKey(
#         Accounts,
#         on_delete=models.CASCADE,
#         related_name='doctor_appointments',
#         limit_choices_to={'is_doctor': True}  # Ensures only doctors can be chosen
#     )
#     patient = models.ForeignKey(
#         Accounts,
#         on_delete=models.CASCADE,
#         related_name='patient_appointments'
#     )
#     date = models.DateTimeField()
#     reason = models.TextField()
#     status = models.BooleanField(default=False)

#     def __str__(self):
#         return f"Appointment for {self.patient} with Dr. {self.doctor} on {self.date.strftime('%Y-%m-%d %H:%M')}"
