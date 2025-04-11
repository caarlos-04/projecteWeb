from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def info_artist_view(request):
    return render(request, 'artist_info.html')