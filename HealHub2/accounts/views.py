from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm


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
        form = UserCreationForm(request.POST)
        return render(request, "accounts/signup.html", {'form': form})
    else:
        # Initialize an empty form
        form = UserCreationForm()
    # Render the signup form
    return render(request, "accounts/signup.html", {'form': form})



def dashboard(response, id):
    """
    Fetches the user with the given ID and renders the dashboard page with the user's details.

    Args:
        response (HttpResponse): The HTTP response instance.
        id (int): The ID of the user.

    Returns:
        HttpResponse: The HTTP response. Renders the dashboard page with the user's details.
    """
    # Fetch the user with the given ID
    user = user.objects.get(id=id)
    # Extract the user's details
    first_name = user.first_name
    last_name = user.last_name
    contact_list = user.contact_list.all()
    # Render the dashboard page with the user's details
    return render(response, "accounts/dashboard.html", {'first_name': first_name, 'last_name': last_name, 'contact_list': contact_list, 'is_doctor': user.is_doctor})


