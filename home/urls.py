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

    path('toggle/<int:task_id>/', views.toggle_task, name='toggle_task'),
    path('delete/<int:task_id>/', views.delete_task, name='delete_task'),
    path('delete_completed/', views.delete_completed_tasks, name='delete_completed'),
]
