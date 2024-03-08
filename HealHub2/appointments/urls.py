from django.urls import path
from .views import user_appointments, create_appointment

urlpatterns = [
    path('appointments', user_appointments, name='appointments'),
    path('appointments/create/', create_appointment, name='create_appointment'),
]
