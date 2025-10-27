from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_login, name='login'),
    path('home/', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('logout/', views.logoutview, name='logout'),
    path('reset/', views.reset, name='reset'),
    path('message/<str:reset_id>/', views.reset_message, name='message'),
    path('new_password/<str:reset_id>/', views.new_pass, name='newpass'),
]
