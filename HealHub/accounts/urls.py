from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.home, name='home'),
    path("", include('django.contrib.auth.urls')),
    path("home/", views.home, name='home'),
    path('dashboard/<int:id>', views.dashboard, name='dashboard'),
    path('signup/', views.signup, name='signup'),
    path('register/', views.register, name='register'),

]
