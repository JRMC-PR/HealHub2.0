from django.shortcuts import render
from django.http import HttpResponse
from.models import Accounts
from .forms import SignupForm

# Create your views here.

def home(response):
    form = SignupForm()
    return render(response, "accounts/home.html", {"form": form})


def dashboard(response, id):
    user = Accounts.objects.get(id=id)
    first_name = user.first_name
    last_name = user.last_name
    if user.is_doctor:
        return render(response, "accounts/dashboard.html", {'first_name': first_name, 'last_name': last_name})
    else:
      return HttpResponse('<h1>WELCOME TO YOUR DASHBOARD %s %s!</h1>' % (first_name, last_name))





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
