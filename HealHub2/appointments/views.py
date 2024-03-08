from .forms import AppointmentForm
from .models import Appointment
from accounts.models import Profile
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db import models
from django.core.mail import send_mail
from django.conf import settings

@login_required  # Ensures that only logged-in users can access this view
def create_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user  # Set the logged-in user as the patient
            appointment.phone = request.user.profile.phone
            appointment.save()  # Now save the appointment to the database
            form.save_m2m()  # Required for saving many-to-many relationships, if any (e.g., if you later add such fields to your model)
                        # Construct and send the email notification
            subject = 'New Appointment Scheduled'
            message = f'''
            Hi,

            An appointment has been scheduled:

            Patient: {appointment.patient.get_full_name()} (Phone: {appointment.phone})
            Doctor: {appointment.doctor.get_full_name()}
            Date: {appointment.date}
            Time: {appointment.time}
            Description: {appointment.description}

            Regards,
            Your Healthcare System
            '''

            # Email is sent to both the patient and the doctor
            recipient_list = [appointment.patient.email, appointment.doctor.email]
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                recipient_list,
                fail_silently=False,
            )
            return redirect('appointments')  # Assuming you have a success URL
    else:
        form = AppointmentForm()
    return render(request, 'appointments/create_appointment.html', {'form': form})

@login_required
def user_appointments(request):
    # Get the current user's profile to check if they are a doctor
    user_profile = Profile.objects.get(user=request.user)
    is_doctor = user_profile.doctor

    # Get all appointments where the user is either the doctor or the patient
    appointments = Appointment.objects.filter(models.Q(doctor=request.user) | models.Q(patient=request.user))

    context = {
        'appointments': appointments,
        'is_doctor': is_doctor,
    }

    return render(request, 'appointments/appointments.html', context)
