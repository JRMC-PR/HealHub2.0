from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Accounts
from .forms import SignupForm, LoginForm
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def home(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            USERNAME_FIELD = form.cleaned_data["USERNAME_FIELD"]
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            email = form.cleaned_data["email"]
            is_doctor = form.cleaned_data["is_doctor"]
            phone_number = form.cleaned_data["phone_number"]
            password = form.cleaned_data["password1"]
            password2 = form.cleaned_data["password2"]
            user = Accounts(USERNAME_FIELD=form.cleaned_data["USERNAME_FIELD"],
                            first_name=form.cleaned_data["first_name"],
                            last_name=form.cleaned_data["last_name"],
                            email=form.cleaned_data["email"],
                            is_doctor=form.cleaned_data["is_doctor"],
                            phone_number=form.cleaned_data["phone_number"],
                            password=form.cleaned_data["password1"],)
            user.save()

            return redirect("dashboard", id=user.id)
    else:
        form = SignupForm()
    return render(request, "accounts/home.html", {'form': form})

def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            USERNAME_FIELD = form.cleaned_data["USERNAME_FIELD"]
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            email = form.cleaned_data["email"]
            is_doctor = form.cleaned_data["is_doctor"]
            phone_number = form.cleaned_data["phone_number"]
            password = form.cleaned_data["password1"]
            password2 = form.cleaned_data["password2"]
            user = Accounts(USERNAME_FIELD=form.cleaned_data["USERNAME_FIELD"],
                            first_name=form.cleaned_data["first_name"],
                            last_name=form.cleaned_data["last_name"],
                            email=form.cleaned_data["email"],
                            is_doctor=form.cleaned_data["is_doctor"],
                            phone_number=form.cleaned_data["phone_number"],
                            password=form.cleaned_data["password1"],)
            user.save()

            return redirect("dashboard", id=user.id)
    else:
        form = SignupForm()
    return render(request, "accounts/signup.html", {'form': form})


def dashboard(response, id):
    user = Accounts.objects.get(id=id)
    first_name = user.first_name
    last_name = user.last_name
    contact_list = user.contact_list.all()
    # if user.is_doctor:
    return render(response, "accounts/dashboard.html", {'first_name': first_name, 'last_name': last_name, 'contact_list': contact_list, 'is_doctor': user.is_doctor})
    # else:
    # return HttpResponse('<h1>WELCOME TO YOUR DASHBOARD %s %s!</h1>' % (first_name, last_name))


def register(response):
    if response.method == "POST":
        form = UserCreationForm(response.POST)
        if form.is_valid():
            form.save()
    else:
        form = UserCreationForm()
    return render(response, "accounts/login.html", {"form": form})



# from django.shortcuts import render
# from django.contrib.auth.decorators import login_required

# @login_required
# def dashboard(request):
#     # Assuming the logged-in user is a Doctor or Patient
#     user = request.user

#     if user.is_doctor:
#         # Render the doctor dashboard if user is a doctor
#         return render(request, 'doctor_dashboard.html')
#     else:
#         # Render the patient dashboard if user is not a doctor
#         return render(request, 'patient_dashboard.html')
