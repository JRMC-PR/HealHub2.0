from .forms import AppointmentForm
from .models import Appointment
from accounts.models import Profile
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db import models
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from django.views.decorators.http import require_POST
from django.contrib import messages


@login_required(login_url='login')
def create_appointment(request):
    """
    This function handles the creation of an appointment.
    It uses the AppointmentForm to validate the input and save the appointment.
    It also sends an email notification to both the patient and the doctor.
    """
    # Pass 'user' to AppointmentForm to adjust fields based on the user's role
    form = AppointmentForm(request.POST or None, user=request.user)

    if request.method == 'POST' and form.is_valid():
        appointment = form.save(commit=False)

        # Set the patient or doctor based on the user's role
        if request.user.profile.doctor:
            appointment.doctor = request.user
            # The 'user' field in form acts as 'patient' for doctors
        else:
            appointment.patient = request.user
            # The 'user' field in form acts as 'doctor' for patients

        appointment.save()  # Save the appointment instance to the database
        form.save_m2m()  # Save many-to-many data for the form

        # Email content setup
        subject = 'New Appointment Scheduled'
        message = f'''
        Hi,

        An appointment has been scheduled:

        Patient: {appointment.patient.get_full_name()} (Phone: {appointment.patient.profile.phone})
        Doctor: {appointment.doctor.get_full_name()}
        Date: {appointment.date}
        Time: {appointment.time}
        Description: {appointment.description}

        Regards,
        Your HealHub2.0 team
        '''
        recipient_list = [appointment.patient.email, appointment.doctor.email]  # Sending email to both doctor and patient

        # Send email notification
        send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list, fail_silently=False)

        return redirect('appointments')  # Redirect to a page showing all appointments

    return render(request, 'appointments/create_appointment.html', {'form': form})


@login_required(login_url='login')
def user_appointments(request):
    """
    This function handles the user appointments view.
    It fetches all appointments where the user is either the doctor or the patient.
    The appointments are then passed to the appointments template.
    """
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

@login_required
@require_POST
def delete_appointments(request):
    """
    This function handles the deletion of an appointment.
    It receives a POST request with the appointment id and deletes the appointment
    if the current user is either the patient or the doctor associated with the appointment.
    """
    appointment_id = request.POST.get('appointment_id')
    if appointment_id:
        try:
            # Try to get the appointment where the current user is either the patient or the doctor
            appointment = Appointment.objects.get(id=appointment_id)
            if appointment.patient == request.user or appointment.doctor == request.user:
                appointment.delete()
                messages.success(request, "Appointment deleted successfully.")
            else:
                messages.error(request, "You do not have permission to delete this appointment.")
        except Appointment.DoesNotExist:
            messages.error(request, "Appointment not found.")
    else:
        messages.error(request, "No appointment ID provided.")

    return redirect('appointments')
