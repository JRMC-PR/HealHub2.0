from django.shortcuts import render, redirect
from .forms import AppointmentForm

def create_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('create_appointment')  # Redirect to a confirmation page or the appointment list
    else:
        form = AppointmentForm()
    return render(request, 'appointments/create_appointment.html', {'form': form})
