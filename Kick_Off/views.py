from django.shortcuts import redirect, render
from . forms import SignupForm, LoginForm
from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'index.html')


# def search(request):
#     search_result = request.GET.get('search_query')
#     return render(request, 'index.html', {'search_result': search_result})


# @login_required(login_url="participants_login")
# def book_now(request, id):
#     if request.user.is_authenticated:
#         return render(request, 'book_now.html')
#     return redirect('login')


# def participants_signup(request):
#     if request.user.is_authenticated:
#         return redirect('')
#     if request.method == 'POST':
#         form = SignupForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.is_participant = True
#             user.save()
#             return redirect('login')
#     form = SignupForm()
#     return render(request, 'participants_signup.html', {'signup_form': form})


# def participants_login(request):
#     if request.user.is_authenticated:
#         return redirect('')
#     if request.method == 'POST':
#         form = LoginForm(request, data=request.POST)
#         if form.is_valid():
#             username = request.POST.get('username')
#             password = request.POST.get('password')
#             user = authenticate(request, username=username, password=password)
#             if user is not None:
#                 auth.login(request, user)
#                 next_url = request.GET.get('next', '')
#                 return redirect(next_url)
#     form = LoginForm()
#     return render(request, 'participants_login.html', {'login_form': form})


# def organisations_signup(request):
#     if request.user.is_authenticated:
#         return redirect('')
#     if request.method == 'POST':
#         form = SignupForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.is_participant = True
#             user.save()
#             return redirect('organisations_login')
#     form = SignupForm()
#     return render(request, 'organisations_signup.html', {'signup_form': form})


# def organisations_login(request):
#     if request.user.is_authenticated:
#         return redirect('')
#     if request.method == 'POST':
#         form = LoginForm(request, data=request.POST)
#         if form.is_valid():
#             username = request.POST.get('username')
#             password = request.POST.get('password')
#             user = authenticate(request, username=username, password=password)
#             if user is not None:
#                 auth.login(request, user)
#                 next_url = request.GET.get('next', '')
#                 return redirect(next_url)
#     form = LoginForm()
#     return render(request, 'organisations_login.html', {'login_form': form})


# def logout(request):
#     if request.user.is_authenticated:
#         return redirect('')
#     auth.logout(request)
#     return redirect('')
