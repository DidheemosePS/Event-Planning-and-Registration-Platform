from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class CustomUser(AbstractUser):
    is_organisation = models.BooleanField(default=False)
    is_participant = models.BooleanField(default=False)


class Event(models.Model):
    event_name = models.CharField(max_length=100)
    event_venue_name = models.CharField(max_length=100)
    event_description = models.TextField()
    event_date = models.DateField()
    event_time = models.TimeField()
    event_number_of_tickets = models.IntegerField()
    event_location_link = models.URLField(max_length=200)
    organisation = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='events_created')


class Cart(models.Model):
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name="event")
    participant = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="cart")
