from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Profile
from appointments.models import Appointment
from django.utils import timezone
from datetime import timedelta


# home view
def home(request):
    """
    Renders the home page.

    Args:
        request (HttpRequest): The HTTP request instance.

    Returns:
        HttpResponse: The HTTP response. Renders the home page.
    """
    return render(request, "accounts/home.html")


# signup view
def signup(request):
    """
    Handles the signup process. If the request method is POST, it validates the form data and creates a new user account.
    If the request method is not POST, it initializes an empty form.

    Args:
        request (HttpRequest): The HTTP request instance.

    Returns:
        HttpResponse: The HTTP response. Redirects to the dashboard if the form is valid and the user is created successfully.
        Otherwise, it renders the signup form.
    """
    # Check if the request method is POST
    if request.method == "POST":
        # Initialize the form with the POST data
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Create a new user
            user = form.save()
            # Authenticate the user
            login(request, user)

            return redirect('profile') # Redirect to the profile page
    else:
        # Initialize an empty form
        form = RegisterForm()
    # Render the signup form
    return render(request, "accounts/signup.html", {'form': form})




@login_required
def profile(request):
    # Get the current user's profile to check if they are a doctor
    user_profile, created = Profile.objects.get_or_create(user=request.user)
    is_doctor = user_profile.doctor

    # Calculate the date two weeks from now
    two_weeks_ahead = timezone.now().date() + timedelta(weeks=2)

    # Filter appointments up to two weeks ahead where the user is either the doctor or the patient
    appointments = Appointment.objects.filter(
        Q(doctor=request.user) | Q(patient=request.user),
        date__lte=two_weeks_ahead
    ).order_by('date', 'time')  # Ordering appointments by date and time

    context = {
        'appointments': appointments,
        'is_doctor': is_doctor,
    }

    return render(request, 'accounts/profile.html', context)

