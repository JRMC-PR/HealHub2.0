from django.shortcuts import render, redirect
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
        print(form.data)
        if form.is_valid():
            form.save()
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

    # Extract the user's details
    first_name = user.first_name
    last_name = user.last_name
    doctor = user.is_staff

    # Render the dashboard page with the user's details
    return render(request, "accounts/dashboard.html", {'first_name': first_name, 'last_name': last_name}, {'doctor': doctor})


def profile(request):
    return render(request, "accounts/profile.html")

