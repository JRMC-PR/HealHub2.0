from appointments.models import Appointment
from .forms import RegisterForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
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



def profile(request):
    if request.user.is_authenticated:
            # Get the current date and time
            now = timezone.now()
            # Calculate the date 2 weeks from now
            two_weeks_later = now + timedelta(weeks=2)

            # Assuming your Appointment model has a 'date' field for the appointment date
            # Adjust the filter according to your Appointment model's fields
            # This query fetches appointments within the next 2 weeks for the current user, either as doctor or patient
            appointments = Appointment.objects.filter(
                date__range=(now, two_weeks_later),
            ).filter(
                doctor=request.user
            ) | Appointment.objects.filter(
                date__range=(now, two_weeks_later),
            ).filter(
                patient=request.user
            )

            context = {
                'appointments': appointments,
            }

            return render(request, "accounts/profile.html", context)
    else:
            # If the user is not authenticated, you can decide how to handle it
        return render(request, "accounts/profile.html")

