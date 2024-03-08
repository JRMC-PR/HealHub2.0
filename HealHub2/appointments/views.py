from django.shortcuts import render, redirect
from .forms import AppointmentForm
from django.contrib.auth.decorators import login_required

@login_required  # Ensures that only logged-in users can access this view
def create_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user  # Set the logged-in user as the patient
            appointment.save()  # Now save the appointment to the database
            form.save_m2m()  # Required for saving many-to-many relationships, if any (e.g., if you later add such fields to your model)
            return redirect('appointment_success')  # Assuming you have a success URL
    else:
        form = AppointmentForm()
    return render(request, 'appointments/create_appointment.html', {'form': form})

