from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect
from django.utils.timezone import now
from .forms import RegisterForm


# Create your views here.

def home(request):
    context = {
        "timestamp": now().timestamp(),
        "spotify_connected": hasattr(request.user, 'social_auth') and request.user.social_auth.filter(provider='spotify').exists() if request.user.is_authenticated else False
    }
    return render(request, 'home.html', context)

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

def about_us_view(request):
    return render(request, "about_us.html")

@login_required
def base_music_view(request):
    return render(request, "music.html")

@login_required
def base_info_view(request):
    return render(request, "info.html")

@login_required(login_url='login')
def music(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'music/music.html')

@login_required(login_url='login')
def playlists(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'music/playlists.html')

@login_required(login_url='login')
def info(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'music/info.html')


