from .models import Event
from django.shortcuts import render, redirect
from django.shortcuts import redirect, render
from . forms import SignupForm, LoginForm, CreateEventsForm
from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required


def index(request):
    events = Event.objects.all()
    return render(request, 'index.html', {'events': events})


def search(request):
    search_result = request.GET.get('search_query')
    return render(request, 'index.html', {'search_result': search_result})


@login_required(login_url="login")
def book_now(request, id):
    event_details = Event.objects.filter(id=id)[0]
    return render(request, 'book_now.html', {'event_details': event_details})


def signup(request):
    if request.user.is_authenticated:
        return redirect('')
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            if form.cleaned_data['account_type'] == 'Participant':
                user.is_participant = True
            if form.cleaned_data['account_type'] == 'Organisation':
                user.is_organisation = True
            user.save()
            return redirect('login')
    form = SignupForm()
    return render(request, 'signup.html', {'signup_form': form})


def login(request):
    if request.user.is_authenticated:
        return redirect('')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                auth.login(request, user)
                next_url = request.GET.get('next', '')
                return redirect(next_url)
    form = LoginForm()
    return render(request, 'login.html', {'login_form': form})


def logout(request):
    auth.logout(request)
    return redirect('')


@login_required(login_url="login")
def create_events(request):
    if not request.user.is_authenticated and not request.user.is_organization:
        return redirect('login')
    if request.method == 'POST':
        form = CreateEventsForm(request.POST)
        if form.is_valid():
            new_event = Event(
                event_name=form.cleaned_data['event_name'],
                event_venue_name=form.cleaned_data['event_venue_name'],
                event_description=form.cleaned_data['event_description'],
                event_date=form.cleaned_data['event_date'],
                event_time=form.cleaned_data['event_time'],
                event_number_of_tickets=form.cleaned_data['event_number_of_tickets'],
                event_location_link=form.cleaned_data['event_location_link'],
                organisation=request.user
            )
            new_event.save()
            return redirect('view_scheduled_events')
    form = CreateEventsForm()
    return render(request, 'create_events.html', {'create_events_form': form})


@login_required(login_url="login")
def view_scheduled_events(request):
    if not request.user.is_authenticated and not request.user.is_organization:
        return redirect('login')
    return render(request, 'view_scheduled_events.html')
