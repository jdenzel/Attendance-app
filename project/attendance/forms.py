from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True) # Includes email field into the django user model. 
    # Add more fields here
    
    class Meta: 
        model = User
        fields = ["username", "first_name", "last_name", "email", "password1", "password2"]
        