from django.urls import path
from .views import create_appointment

urlpatterns = [
    path('appointments/create/', create_appointment, name='create_appointment'),
]
