from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
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
def signup(response):
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
    if response.method == "POST":
        # Initialize the form with the POST data
        form = RegisterForm(response.POST)
        if form.is_valid():
            print(form.cleaned_data)
            user = form.save()
            return redirect('dashboard' , username = user.username)
        else:
            print(form.errors)
    else:
        # Initialize an empty form
        form = RegisterForm()
    # Render the signup form
    return render(response, "accounts/signup.html", {'form': form})



from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User

def dashboard(request, username):
    # Fetch the user with the given username
    user = get_object_or_404(User, username=username)

    # Prepare context data
    context = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'doctor': user.profile.doctor,  # Assuming doctor info is stored in Profile model
    }

    # Render the dashboard page with the user's details
    return render(request, "accounts/dashboard.html", context)


def profile(request):
    return render(request, "accounts/profile.html")

