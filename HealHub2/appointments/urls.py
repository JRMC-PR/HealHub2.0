from django.urls import path
from .views import user_appointments, create_appointment, delete_appointments


urlpatterns = [
    path('appointments', user_appointments, name='appointments'),
    path('appointments/create/', create_appointment, name='create_appointment'),
    path('appointments/delete_appointment/', delete_appointments, name='delete_appointments'),
]
