from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_login, name='login'),
    path('home/', views.home, name='home'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
]
