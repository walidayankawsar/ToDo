from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

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
            print("❌ Error set হলো:", error)

    return render(request, "registration/login.html", {"error": error})


@login_required
def home(request):
    return render(request, "ToDo.html")

def user_logout(request):
    logout(request)
    return redirect("login")

