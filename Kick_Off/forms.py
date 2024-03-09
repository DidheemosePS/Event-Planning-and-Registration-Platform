from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from Kick_Off.models import CustomUser
from django import forms
from django.forms.widgets import PasswordInput, TextInput

# Signup / Create a user form


class SignupForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

# Login form


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())
