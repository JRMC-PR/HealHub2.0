from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.home, name='home'),
    path("", include('django.contrib.auth.urls')),
    path("home/", views.home, name='home'),
    path('dashboard/<str:username>/', views.dashboard, name='dashboard'),
    path('signup/', views.signup, name='signup'),
    path('', include('django.contrib.auth.urls')),

]
