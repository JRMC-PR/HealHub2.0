from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import RegisterForm


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
    return render(request, "accounts/profile.html")

