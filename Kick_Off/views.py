import json
from django.http import HttpResponse, JsonResponse
from .models import Event, Cart, Ticket
from django.shortcuts import render, redirect
from django.shortcuts import redirect, render
from . forms import SignupForm, LoginForm, CreateEventsForm
from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.db.models import Q, F, Sum
from django.utils.timezone import now


def index(request):
    # event_date___gte used to find the events available in future, To avoid the expried events and __gte means '>='
    today = now().date()
    events = Event.objects.filter(event_date__gte=today).annotate(
        booked_tickets=Sum('ticket_events__event_number_of_tickets')).values(
        'id', 'event_name', 'event_venue_name', 'event_date', 'event_time', 'booked_tickets').order_by('-updated')
    return render(request, 'index.html', {'title': 'Kick Off', 'page_url': "book_now", 'events': events})


def search(request):
    # event_date___gte used to find the events available in future, To avoid the expried events and __gte means '>='
    today = now().date()
    search_value = request.GET.get('search_query')
    # Q is used to perform OR logical operation
    search_result = Event.objects.filter(Q(event_date__gte=today) & Q(event_name__icontains=search_value) | Q(event_venue_name__icontains=search_value) | Q(organisation_name__icontains=search_value)).annotate(
        booked_tickets=Sum('ticket_events__event_number_of_tickets')).values(
        'id', 'event_name', 'event_venue_name', 'event_date', 'event_time', 'booked_tickets').order_by('-updated')
    return render(request, 'index.html', {'title': 'Search - Kick Off', 'page_url': "book_now", 'events': search_result})


@login_required(login_url="login")
def book_now(request, id):
    # event_date___gte used to find the events available in future, To avoid the expried events and __gte means '>='
    today = now().date()
    event_details = Event.objects.filter(event_date__gte=today, id=id)
    if not event_details:
        return HttpResponse("This event is not available")
    book_mark = Cart.objects.filter(
        participant=request.user, event=Event.objects.get(pk=id))
    if not book_mark:
        return render(request, 'book_now.html', {'event_details': event_details[0]})
    return render(request, 'book_now.html', {'title': 'Book Now - Kick Off', 'event_details': event_details[0], 'book_mark': True})


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
    return render(request, 'signup.html', {'title': 'Signup - Kick Off', 'signup_form': form})


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
    return render(request, 'login.html', {'title': 'Login - Kick Off', 'login_form': form})


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
            create_event.organisation_name = request.user
            create_event.organisation = request.user
            create_event.save()
            return redirect('view_scheduled_events')
    form = CreateEventsForm()
    return render(request, 'create_events.html', {'title': 'Create Event - Kick Off', 'create_events_form': form, 'submit_button_value': "Create"})


@login_required(login_url="login")
def view_scheduled_events(request):
    if not request.user.is_organisation:
        return redirect('login')
    view_scheduled_events = Event.objects.filter(organisation=request.user).annotate(booked_tickets=Sum(
        'ticket_events__event_number_of_tickets')).values('id', 'event_name', 'event_venue_name', 'event_date', 'event_time', 'booked_tickets').order_by('-updated')
    return render(request, 'index.html', {'title': 'Scheduled Events - Kick Off', 'page_url': "view_scheduled_event_details", 'events': view_scheduled_events})


@login_required(login_url="login")
def view_scheduled_event_details(request, id):
    if not request.user.is_organisation:
        return redirect('login')
    view_scheduled_event_details = Event.objects.filter(
        organisation=request.user, id=id)[0]
    return render(request, 'book_now.html', {'title': 'Scheduled Event Details - Kick Off', 'organisation_id': request.user.id, 'event_details': view_scheduled_event_details})


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
    fetch_saved_events = Event.objects.filter(
        cart_events__participant=request.user).values(
        'id', 'event_name', 'event_venue_name', 'event_date', 'event_time').order_by('-updated')
    if not fetch_saved_events:
        return HttpResponse('No saved events')
    return render(request, 'index.html', {'title': 'Saved Events - Kick Off', 'page_url': "book_now", 'events': fetch_saved_events})


@login_required(login_url="login")
def book_tickets(request, id):
    if not request.user.is_participant:
        return redirect('login')
    # event_date___gte used to find the events available in future, To avoid the expried events and __gte means '>='
    today = now().date()
    ticket_details = Event.objects.filter(event_date__gte=today, id=id).values(
        'id', 'event_name', 'event_venue_name', 'event_date', 'event_time', 'event_number_of_tickets', 'event_ticket_price')
    if not ticket_details:
        return HttpResponse("This event is not available")
    ticket_count = ticket_details[0]['event_number_of_tickets']
    if ticket_count == 0:
        return HttpResponse("No tickets left")
    return render(request, 'book_tickets.html', {'title': 'Book Tickets - Kick Off', 'ticket_details': ticket_details[0]})


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
    return render(request, 'create_events.html', {'title': 'Scheduled Event Edit - Kick Off', 'create_events_form': form, 'event_edit': event_edit, 'submit_button_value': "Update"})


@login_required(login_url="login")
def make_payment(request, id):
    if not request.user.is_participant:
        return JsonResponse({'login_required': True})
    if request.method == 'POST':
        # json.loads(request.POST) used to get the data from the POST request, request.POST can be used only in the form submissions
        Ticket.objects.create(
            event=Event.objects.get(pk=id), participant=request.user, event_number_of_tickets=json.loads(request.body)['event_number_of_tickets'], event_ticket_price=json.loads(request.body)['event_ticket_price'])
        Event.objects.filter(id=id).update(event_number_of_tickets=F(
            'event_number_of_tickets')-json.loads(request.body)['event_number_of_tickets'])
        return JsonResponse({'payment_status': True})
    return JsonResponse({'status': 'Invalid request'})


@login_required(login_url="login")
def tickets_booked(request):
    if not request.user.is_participant:
        return redirect('login')
    fetch_tickets_booked = Event.objects.filter(ticket_events__participant=request.user).annotate(
        number_of_tickets=F('ticket_events__event_number_of_tickets'),
        ticket_price=F('ticket_events__event_ticket_price'),
        ticket_created=F('ticket_events__created')).order_by('-ticket_events__created').values(
        'id', 'event_name', 'event_venue_name', 'event_date', 'event_time', 'number_of_tickets', 'ticket_price', 'ticket_created')
    if not fetch_tickets_booked:
        return HttpResponse('No tickets booked yet')
    return render(request, 'tickets_booked.html', {
        'title': 'Tickets Booked - Kick Off', 'ticket_details': fetch_tickets_booked, 'text': "Amount Paid"
    })
