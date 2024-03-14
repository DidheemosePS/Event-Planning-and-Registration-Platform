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
    return render(request, 'index.html', {'page_url': "book_now", 'events': events})


def search(request):
    search_value = request.GET.get('search_query')
    # Q is used to perform OR logical operation
    search_result = Event.objects.filter(Q(event_name=search_value) | Q(
        event_venue_name=search_value) | Q(organisation_name=search_value))
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
        return render(request, 'signup.html', {'signup_form': form})
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
        return render(request, 'login.html', {'login_form': form})
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
            create_event = form.save(commit=False)
            create_event.organisation = request.user
            create_event.save()
            return redirect('view_scheduled_events')
    form = CreateEventsForm()
    return render(request, 'create_events.html', {'create_events_form': form, 'submit_button_value': "Create"})


@login_required(login_url="login")
def view_scheduled_events(request):
    if not request.user.is_organisation:
        return redirect('login')
    view_scheduled_events = Event.objects.filter(organisation=request.user)
    return render(request, 'index.html', {'page_url': "view_scheduled_event_details", 'events': view_scheduled_events})


@login_required(login_url="login")
def view_scheduled_event_details(request, id):
    if not request.user.is_organisation:
        return redirect('login')
    view_scheduled_event_details = Event.objects.filter(
        organisation=request.user, id=id)[0]
    return render(request, 'book_now.html', {'organisation_id': request.user.id, 'event_details': view_scheduled_event_details})


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
    return render(request, 'index.html', {'page_url': "book_now", 'events': [fetch_saved_events[0].event]})


@login_required(login_url="login")
def book_tickets(request, id):
    if not request.user.is_participant:
        return redirect('login')
    ticket_count = Event.objects.filter(id=id)[0]
    if ticket_count.event_number_of_tickets == 0:
        return HttpResponse("No tickets left")
    return render(request, 'book_tickets.html')


@login_required(login_url="login")
def view_scheduled_event_details_delete(request, id):
    if not request.user.is_organisation:
        return redirect('login')
    Event.objects.filter(organisation=request.user, id=id).delete()
    return redirect('view_scheduled_events')


@login_required(login_url="login")
def view_scheduled_event_details_edit(request, id):
    if not request.user.is_organisation:
        return redirect('login')
    event_edit = Event.objects.filter(organisation=request.user, id=id)[0]
    if request.method == 'POST':
        form = CreateEventsForm(request.POST, instance=event_edit)
        if form.is_valid():
            form.save()
            return redirect('view_scheduled_events')
    form = CreateEventsForm(instance=event_edit)
    return render(request, 'create_events.html', {'create_events_form': form, 'event_edit': event_edit, 'submit_button_value': "Update"})
