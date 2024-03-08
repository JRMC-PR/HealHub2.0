from .forms import AppointmentForm
from .models import Appointment
from accounts.models import Profile
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db import models

@login_required  # Ensures that only logged-in users can access this view
def create_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user  # Set the logged-in user as the patient
            appointment.phone = request.user.profile.phone # Set the phone field to the user's phone
            appointment.save()  # Now save the appointment to the database
            form.save_m2m()  # Required for saving many-to-many relationships, if any (e.g., if you later add such fields to your model)
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
