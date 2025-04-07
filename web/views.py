from django.shortcuts import render
from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect
from django.utils.timezone import now
from .forms import RegisterForm

# Create your views here.

def home(request):
    return render(request, 'home.html', {"timestamp": now().timestamp()})

def logout_view(request):
    auth_logout(request)
    return redirect('home')

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form})

