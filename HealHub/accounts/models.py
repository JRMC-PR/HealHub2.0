#!/usr/bin/python3
"""Here lives the basic user model
    for the project

    django user cmodels comes with these default fields
    """
from django.db import models
import uuid


def unique_username():
    """Generates a unique username"""
    return f"username{uuid.uuid4().hex[:40]}"


class Accounts(models.Model):
    """This is the custom user model"""
    #pulic fields for the user
    USERNAME_FIELD = models.CharField(max_length=40, default=unique_username)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    password = models.CharField(max_length=200, default="password")
    phone_number = models.CharField(max_length=200)
    contact_list = models.ManyToManyField("self", blank=True)
    office_address = models.CharField(max_length=200, default="None")
    is_doctor = models.BooleanField(default=False)
    specialty = models.CharField(max_length=200, default="General")
    created_at = models.DateTimeField(auto_now_add=True) #This sets the time of creation
    updated_at = models.DateTimeField(auto_now=True) #This updates the time of modification

    def __str__(self):
        """Returns the user's full name, email, phone number and if they are a doctor or not"""
        return f"{self.first_name} {self.last_name} {self.email} {self.phone_number} {self.is_doctor}"



