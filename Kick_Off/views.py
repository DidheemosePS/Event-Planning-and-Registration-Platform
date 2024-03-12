import json
from django.http import HttpResponse, JsonResponse
from .models import Event, Cart
from django.shortcuts import render, redirect
from django.shortcuts import redirect, render
from . forms import SignupForm, LoginForm, CreateEventsForm
from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.db.models import Q


def index(request):
    events = Event.objects.all()
    return render(request, 'index.html', {'events': events})


def search(request):
    search_value = request.GET.get('search_query')
    # Q is used to perform OR logical operation
    search_result = Event.objects.filter(Q(event_name=search_value) | Q(
        event_venue_name=search_value))
    return render(request, 'index.html', {'events': search_result})


@login_required(login_url="login")
def book_now(request, id):
    event_details = Event.objects.filter(id=id)[0]
    book_mark = Cart.objects.filter(
        participant=request.user, event=Event.objects.get(pk=id))
    if not book_mark:
        return render(request, 'book_now.html', {'event_details': event_details})
    return render(request, 'book_now.html', {'event_details': event_details, 'book_mark': True})


def signup(request):
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
    if not request.user.is_organisation:
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
    if not request.user.is_organisation:
        return redirect('login')
    view_scheduled_events = Event.objects.filter(organisation=request.user)
    return render(request, 'index.html', {'events': view_scheduled_events})


def save_this_event(request):
    if not request.user.is_participant:
        return JsonResponse({'login_required': True})
    if request.method == 'POST':
        # json.loads(request.POST) used to get the data from the POST request, request.POST can be used only in the form submissions
        id = json.loads(request.body)['id']
        # event = Event.objects.get(pk=id) to create Event model instance
        if not Cart.objects.filter(participant=request.user, event=Event.objects.get(pk=id)):
            Cart.objects.create(
                participant=request.user, event=Event.objects.get(pk=id))
            return JsonResponse({'bookmarked': True})
        else:
            Cart.objects.filter(
                participant=request.user, event=Event.objects.get(pk=id)).delete()
            return JsonResponse({'bookmarked': False})
    return JsonResponse({'status': 'Invalid request'})


@login_required(login_url="login")
def saved_events(request):
    if not request.user.is_participant:
        return redirect('login')
    fetch_saved_events = Cart.objects.filter(participant=request.user)
    if not fetch_saved_events:
        return HttpResponse('No saved events')
    # [fetch_saved_events[0].event] convert to array
    return render(request, 'index.html', {'events': [fetch_saved_events[0].event]})
