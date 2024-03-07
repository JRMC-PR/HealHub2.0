from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Your additional fields
    doctor = models.BooleanField(default=False)  # Doctor field, default to False
    specialty = models.CharField(max_length=100, blank=True, null=True)  # Specialty field, can be empty

    def __str__(self):
        return self.user.username

# Signal to create or update the user profile
@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
