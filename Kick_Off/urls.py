from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name=""),
#     path('book_now/<str:id>/', views.book_now, name='book_now'),
#     path('search/', views.search, name='search'),
#     path('participants_signup/', views.participants_signup,
#          name='participants_signup'),
#     path('participants_login/', views.participants_login,
#          name='participants_login'),
#     path('organisations_signup/', views.organisations_signup,
#          name='organisations_signup'),
#     path('organisations_login/', views.organisations_login,
#          name='organisations_login'),
#     path('logout/', views.logout, name='logout'),
]
