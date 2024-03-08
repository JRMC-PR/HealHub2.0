from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.home, name='home'),
    path("", include('django.contrib.auth.urls')), #
    path("home/", views.home, name='home'), #directs to the homepage view
    path('profile/', views.profile, name='profile'), #directs to the profile view
    path('signup/', views.signup, name='signup'), #directs to the signup view
]
