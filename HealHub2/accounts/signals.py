from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.urls import reverse
from django.template.loader import render_to_string
from django.utils.html import strip_tags

@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        context = {
            'user': instance,
            'login_url': reverse('login')  # Assuming you have a named URL for login
        }
        html_message = render_to_string('emails/welcome_email.html', context)
        plain_message = strip_tags(html_message)
        subject = 'Welcome to HealHub!'

        send_mail(
            subject,
            plain_message,
            'healhub2.0@gmailcom',
            [instance.email],
            html_message=html_message,
            fail_silently=False,
        )
