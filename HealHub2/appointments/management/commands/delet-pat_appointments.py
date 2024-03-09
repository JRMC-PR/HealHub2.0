from django.core.management.base import BaseCommand
from django.utils import timezone
from appointments.models import Appointment
from django.db import models
from datetime import datetime

class Command(BaseCommand):
    help = 'Deletes appointments that have passed'

    def handle(self, *args, **kwargs):
        # Get the current date and time in a timezone-aware manner
        now = timezone.localtime()

        # Combine date and time for each appointment to compare against the current datetime
        appointments_to_delete = Appointment.objects.annotate(
            datetime_combined=models.ExpressionWrapper(
                models.functions.Concat('date', 'time',
                    output_field=models.DateTimeField()),
                output_field=models.DateTimeField()
            )
        ).filter(datetime_combined__lt=now)

        # Delete the filtered appointments
        deleted, _ = appointments_to_delete.delete()

        self.stdout.write(self.style.SUCCESS(f'Successfully deleted {deleted} past appointments'))
