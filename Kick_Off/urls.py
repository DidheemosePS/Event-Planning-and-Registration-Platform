from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name=""),
    path('book_now/<str:id>/', views.book_now, name='book_now'),
    path('search/', views.search, name='search'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('create_events/', views.create_events, name='create_events'),
    path('view_scheduled_events/', views.view_scheduled_events,
         name='view_scheduled_events'),
    path('save_this_event/<str:id>/',
         views.save_this_event, name='save_this_event'),
    path('saved_events/', views.saved_events, name='saved_events'),
]
