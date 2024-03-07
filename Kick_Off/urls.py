from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name=""),
    path('book_now/<str:id>/', views.book_now, name='book_now'),
    path('search/', views.search, name='search'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
]
