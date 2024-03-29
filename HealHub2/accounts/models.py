from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Your additional fields
    doctor = models.BooleanField(default=False)  # Doctor field, default to False
    specialty = models.CharField(max_length=100, blank=True, null=True)  # Specialty field, can be empty
    phone = models.CharField(max_length=15, default='1234567890')  # Phone field with a default value

    def __str__(self):
        return self.user.username

