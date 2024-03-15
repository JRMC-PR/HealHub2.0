from django.contrib.auth import login, authenticate
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from accounts.models import Profile

class RegisterForm(UserCreationForm):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password and fields for Profile model.
    Inherits from UserCreationForm which provides password validation.

    Attributes:
        email (forms.EmailField): Email field.
        doctor_choices (list): List of doctor choices.
        phone (forms.CharField): Phone field.
        doctor (forms.ChoiceField): Doctor field.
        specialty (forms.CharField): Specialty field.

    Methods:
        clean_first_name: Capitalizes the first name.
        clean_last_name: Capitalizes the last name.
        clean_specialty: Capitalizes the specialty.
        save: Overridden save method to create a User instance and a Profile instance.

    """

    email = forms.EmailField(required=True)  # Email field
    doctor_choices = [
        (True, 'Yes'),
        (False, 'No')
    ] # Doctor choices
    phone = forms.CharField(max_length=15, initial='7877512266')

    doctor = forms.ChoiceField(choices=doctor_choices, widget=forms.RadioSelect, help_text="Are you a doctor?")  # Doctor field
    specialty = forms.CharField(required=False, help_text="Specify your specialty if you are a doctor.")  # Specialty field

    class Meta:
        """
        Meta class for RegisterForm. Specifies the model and fields to be used.
        """
        model = User  # The model to use
        fields = ["username", "email", "password1", "password2", "first_name", "last_name"]  # The fields to use

    def clean_first_name(self):
        """
        Capitalizes the first name.

        Returns:
            str: The capitalized first name.
        """
        first_name = self.cleaned_data['first_name']
        # Capitalize first name
        return first_name.capitalize()

    def clean_last_name(self):
        """
        Capitalizes the last name.

        Returns:
            str: The capitalized last name.
        """
        last_name = self.cleaned_data['last_name']
        # Capitalize last name
        return last_name.capitalize()

    def clean_specialty(self):
        """
        Capitalizes the specialty.

        Returns:
            str: The capitalized specialty.
        """
        # Ensure the specialty field is included in cleaned_data
        specialty = self.cleaned_data.get('specialty', '')
        # Capitalize specialty
        return specialty.capitalize()

    def save(self, commit=True):
        """
        Overridden save method. Creates a User instance and a Profile instance.
        If commit is True, it saves the User instance and creates and saves a Profile instance associated with the User.

        Args:
            commit (bool, optional): Determines whether to save the User instance. Defaults to True.

        Returns:
            User: The created User instance.
        """
        user = super().save(commit=False)  # Create User instance
        if commit:
            user.save()  # Save User instance
            doctor_status = self.cleaned_data.get('doctor') == 'True'
            # Create or get Profile instance associated with the User
            Profile.objects.get_or_create(
                user=user,
                defaults={
                    'doctor': doctor_status, # Set doctor field
                    'specialty': self.cleaned_data.get('specialty', ''),  # Set specialty field
                    'phone': self.cleaned_data.get('phone', ''),
                }
            )
        return user  # Return User instance

