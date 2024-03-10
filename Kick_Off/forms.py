from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from Kick_Off.models import CustomUser, Event
from django import forms
from django.forms.widgets import PasswordInput, TextInput

# Signup / Create a user form


class SignupForm(UserCreationForm):
    ACCOUNT_TYPE = [
        ('Participant', 'Participant'),
        ('Organisation', 'Organisation'),
    ]
    account_type = forms.ChoiceField(
        choices=ACCOUNT_TYPE,
        widget=forms.RadioSelect(),
        required=True
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email',
                  'account_type', 'password1', 'password2']

# Login form


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())

# Form to create an event


class CreateEventsForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['event_name', 'event_venue_name', 'event_description',
                  'event_date', 'event_time', 'event_number_of_tickets', 'event_location_link']
        widgets = {
            'event_description': forms.Textarea(attrs={'rows': 5}),
            'event_date': forms.DateInput(attrs={'type': 'date'}),
            'event_time': forms.TimeInput(attrs={'type': 'time'}),
        }
