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
    event_name = forms.CharField(
        label="Event Name", max_length="100", required=True)
    event_venue_name = forms.CharField(
        label="Venue Name", max_length=100, required=True)
    event_description = forms.CharField(
        label="Event Description",
        required=True,
        widget=forms.Textarea(attrs={'rows': 5})
    )
    event_date = forms.DateField(
        label="Event Date", required=True, widget=forms.DateInput(attrs={'type': "date"}))
    event_time = forms.TimeField(
        label="Event Time", required=True, widget=forms.TimeInput(attrs={'type': "time"}))
    event_number_of_tickets = forms.IntegerField(
        label="Tickets Available", required=True)
    event_ticket_price = forms.IntegerField(
        label="Ticket Price", required=True)
    event_location_link = forms.URLField(
        label="Location Link", max_length=200, required=True, widget=forms.DateInput(attrs={'type': "url"}))
    event_image = forms.FileField(label="Image", required=True, widget=forms.FileInput(
        attrs={'type': "file", 'accept': "image/png, image/jpeg"}))
    event_video = forms.FileField(label="Video", required=True, widget=forms.FileInput(
        attrs={'type': "file", 'accept': "video/mp4"}))

    class Meta:
        model = Event
        fields = ['event_name', 'event_venue_name', 'event_description',
                  'event_date', 'event_time', 'event_number_of_tickets', 'event_ticket_price', 'event_location_link']
