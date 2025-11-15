from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import PasswordReset, Task
from django.urls import reverse
from django.core.mail import EmailMessage
from django.conf import settings
from django.utils import timezone

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
            pass_reset_url = request.build_absolute_uri(reverse('newpass', kwargs={'reset_id': new_password_reset.reset_id}))

            # email contant
            url_page = f'Reset your password useing the link below:\n\n\n{pass_reset_url}'

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
    try:
        reset_id = PasswordReset.objects.get(reset_id = reset_id)
    except PasswordReset.DoesNotExist:
        messages.error(request, 'invalid URL')
        return redirect('reset')
    
    if request.method == "POST":
        password_have_error = False
        password =request.POST.get('password')
        confirm_password =request.POST.get('confirm_password')

        if password != confirm_password:
            password_have_error = True
            messages.error(request, 'password dose not match')

        expiration_time = reset_id.created_when + timezone.timedelta(minutes=10)
        
        if timezone.now() > expiration_time:
            password_have_error = True
            messages.error(request, 'Reset link has expired')

        if not password_have_error:
            user = reset_id.user
            user.set_password(password)
            user.save()

            reset_id.delete()
            messages.success(request, 'reset password successfully.')
            return redirect('login')
        else:
            return redirect('reset')
    return render(request, 'new_password.html')


@login_required
def home(request):

    filter_type = request.GET.get('filter', 'all')

    if filter_type == 'completed':
        tasks = Task.objects.filter(user=request.user, is_completed=True)
    elif filter_type == 'imcompleted':
        tasks = Task.objects.filter(user=request.user, is_completed=False)
    elif filter_type == 'important':
        tasks = Task.objects.filter(user=request.user, priority='high')
    else:
        tasks = Task.objects.filter(user=request.user)



    if request.method == 'POST':
        title = request.POST.get('title')
        priority = request.POST.get('priority')

        if title:
            Task.objects.create(user=request.user, title=title, priority=priority)
            messages.success(request, "নতুন কাজ সফলভাবে যোগ হয়েছে!")
            return redirect('home')
        
    completed = Task.objects.filter(user=request.user, is_completed=True).count()
    total = Task.objects.filter(user=request.user).count()
    remaining = total - completed

    context = {
        "completed_task": completed,
        "total_task": total,
        "remaining_task": remaining,
        "filter_type": filter_type,
        "tasks": tasks.order_by('-created_at'),
    }
        
    return render(request, "ToDo.html", context)

@login_required
def toggle_task(request, task_id):
    task = Task.objects.get(user=request.user, id=task_id)
    task.is_completed = not task.is_completed
    task.save()
    return redirect('home')

@login_required
def delete_task(request, task_id):
    task = Task.objects.get(user=request.user, id=task_id)
    task.delete()
    messages.success(request, "কাজটি সফলভাবে মুছে ফেলা হয়েছে।")
    return redirect('home')

@login_required
def delete_completed_tasks(request, task_id):
    task = Task.objects.get(user=request.user, is_completed=True)
    task.delete()
    messages.success(request, "সম্পূর্ণ কাজগুলো মুছে ফেলা হয়েছে।")
    return redirect('home')

@login_required
def logoutview(request):
    logout(request)
    return redirect('login')
