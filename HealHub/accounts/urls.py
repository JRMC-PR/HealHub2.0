from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name='home'),
    path("home/", views.home, name='home'),
    path('dashboard/<int:id>', views.dashboard, name='dashboard'),
    # path('signup/', views.signup, name='signup'),
]
