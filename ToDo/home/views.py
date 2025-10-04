from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

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
