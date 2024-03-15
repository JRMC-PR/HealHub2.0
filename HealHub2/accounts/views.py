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

# TODO: add login required when landing is created
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

# landing view


def landing(request):
    """
    Renders the landing page.

    Args:
        request (HttpRequest): The HTTP request instance.

    Returns:
        HttpResponse: The HTTP response. Renders the landing page.
    """
    team_members = [
        {
            'name': 'Jesus R. Mendez Cruz',
            'title': 'Lead Developer - Fullstack (Backend Focus)',
            'description': 'As the lead developer, I balanced my focus between frontend and backend aspects, emphasizing backend development. My duties encompassed designing and executing efficient server-side applications, enhancing performance, and ensuring responsiveness to frontend requests and multiple APIs. Simultaneously, I contributed to frontend development, aiming for a seamless user experience. This dual focus allowed us to build a robust, user-centered platform, effectively bridging the gap between server efficiency and user interface design.',
            'image': 'static/accounts/images/jesusM.jpg',
            'social_media': {
                'github': 'https://github.com/JRMC-PR',
                'linkedin': 'https://www.linkedin.com/in/jesús-méndez-068b8a27a/'
            }
        },
        {
            'name': 'Juan C. Rodriguez Ocasio',
            'title': 'Fullstack (Frontend Focus)',
            'description': 'As a front-end developer, I specialized in designing key pages, such as the landing and base HTML, pivotal for our web interface. Collaboratively, I helped shape our front-end strategy, ensuring our efforts aligned seamlessly with project objectives. My role extended beyond coding, involving strategic planning to enhance user interaction and satisfaction. This collaborative effort led to a user-friendly and aesthetically pleasing interface, significantly enriching the overall online experienceof the patients and doctors.',
            'image': 'static/accounts/images/juanrod.png',
            'social_media': {
                'github': 'https://github.com/JCRoooD',
                'linkedin': 'https://linkedin.com/in/jcroood/'
            }
        },
        {
            'name': 'Guillermo J. Pereyo Castellvi',
            'title': 'Fullstack (Frontend Focus)',
            'description': 'As a frontend developer, I was deeply involved in architecting the website\'s structure and choosing key components to boost user interaction and system efficiency. My work utilized cutting-edge frontend technologies to achieve a seamless interface, complemented by backend integration for uniformity across the platform. I dedicated myself to enhancing user interactivity, ensuring adaptability in design, and upholding superior web aesthetics, all aimed at fulfilling our project\'s ambitious objectives. This comprehensive approach contributed significantly to a user-friendly and high-performing application.',
            'image': 'static/accounts/images/guillermo_pereyo2.png',
            'social_media': {
                'github': 'https://github.com/GuilleP2018',
                'linkedin': 'https://www.linkedin.com/in/guillermo-pereyo-castellvi-0b3a3b1b3/'
            }
        },
        {
            'name': 'Joshua Santiago Morales',
            'title': 'Fullstack (Backend Focus)',
            'description': ' ',
            'image': '',
            'social_media': {
                'github': 'https://github.com/JCRoooD',
                'linkedin': '#'
            }
        },
    ]
    return render(request, "accounts/landing.html", {'team_members': team_members})


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

            return redirect('profile')  # Redirect to the profile page
    else:
        # Initialize an empty form
        form = RegisterForm()
    # Render the signup form
    return render(request, "accounts/signup.html", {'form': form})


# login view
@login_required(login_url='login')
def profile(request):
    """
    This function handles the profile view.
    It checks if the logged-in user is a doctor and fetches their upcoming appointments
    for the next two weeks. The appointments are then passed to the profile template.
    """
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

    # Prepare the context for the template
    context = {
        'appointments': appointments,
        'is_doctor': is_doctor,
    }

    # Render the profile template with the context
    return render(request, 'accounts/profile.html', context)
