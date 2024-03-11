from django.urls import path
from . import views

urlpatterns = [
    # Other URLs...
    path('search/', views.search_doctors, name='search_doctors'),
]
