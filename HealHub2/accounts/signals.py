from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        html_message = render_to_string('emails/welcome_email.html', {'user': instance})
        plain_message = strip_tags(html_message)
        send_mail(
            'Welcome to HealHub!',
            plain_message,
            'healhub2.0@gmail.com',
            [instance.email],
            fail_silently=False,
            html_message=html_message,  # Pass the HTML version here
        )
