from django.shortcuts import render, redirect
from django.http import HttpResponse
from.models import Accounts
from .forms import SignupForm

# Create your views here.

def home(response):
    if response.method == "POST":
      form = SignupForm(response.POST)
      if form.is_valid():
          first_name = form.cleaned_data["first_name"]
          last_name = form.cleaned_data["last_name"]
          email = form.cleaned_data["email"]
          password = form.cleaned_data["password"]
          confirm_password = form.cleaned_data["confirm_password"]
          is_doctor = form.cleaned_data["is_doctor"]
          phone_number = form.cleaned_data["phone_number"]
          if password == confirm_password:
              user = Accounts(first_name=first_name, last_name=last_name, email=email, password=password, is_doctor=is_doctor, phone_number=phone_number)
              user.save()
              return redirect("dashboard", id=user.id)
          else:
              return HttpResponse('<h1>THE PASSWORDS DO NOT MATCH</h1>')
    else:
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
