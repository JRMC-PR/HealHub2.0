from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.landing, name='landing'), #TODO: Change url to landing page view [JUAN]
    path("", include('django.contrib.auth.urls')), #
    path("home/", views.home, name='home'), #directs to the homepage view
    path('profile/', views.profile, name='profile'), #directs to the profile view
    path('signup/', views.signup, name='signup'), #directs to the signup view
]
