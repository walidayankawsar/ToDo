from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import PasswordReset
from django.urls import reverse
from django.core.mail import EmailMessage
from django.conf import settings

def user_login(request):
    error = None   # শুরুতে error নাই

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("home")
        else:
            error = "Username or password ভুল!" 

    return render(request, "registration/login.html", {"error": error})

def register(request):

    if request.method == 'POST':
        # getting user inputs from frontend
        first_name = request.POST.get('first name')
        last_name = request.POST.get('last name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user_data_has_error = False

        if User.objects.filter(username=username).exists():
            user_data_has_error = True
            messages.error(request, 'Username already exists..')

        if User.objects.filter(email=email).exists():
            user_data_has_error = True
            messages.error(request, 'Email already exists..')

        if not user_data_has_error:
            new_user = User.objects.create_user(
                first_name = first_name,
                last_name = last_name,
                email = email,
                username = username,
                password = password,
            )
            messages.success(request,'Account created. Login now..')
        else:
            return redirect('register')



    return render(request, 'register.html')


def reset(request):
    if request.method == "POST":
        email = request.POST.get('email')

        # verify if email exists
        try:
            user = User.objects.get(email = email)

            # create a new reset id
            new_password_reset = PasswordReset(user=user)
            new_password_reset.save()

            # create a reset url
            pass_reset_url = reverse('newpass', kwargs={'reset_id': new_password_reset.reset_id})

            # email contant
            url_page = f'Reset your password useing the link below:\n\n\n localhost:8000{pass_reset_url}'

            email_message = EmailMessage(
                'Reset your password', # email subject
                url_page,
                settings.EMAIL_HOST_USER, # email sender
                [email] # email  receiver 
            )

            email_message.fail_silently = True
            email_message.send()

            return redirect('message', new_password_reset.reset_id)



        except User.DoesNotExist:
            messages.error(request, f"No User with '{email}' found")
            return redirect('reset')
    return render(request, 'reset.html')


def reset_message(request, reset_id):
    return render(request, 'sent_reset_link.html')


def new_pass(request, reset_id):
    return render(request, 'new_password.html')


@login_required
def home(request):
    return render(request, "ToDo.html")


def logoutview(request):
    logout(request)
    return redirect('login')
