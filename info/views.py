from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
@login_required
def info_artist_view(request):
    return render(request, 'artist_info.html')

@login_required
def redirect_info(request):
    access_token = request.session.get('access_token')

    if access_token:
        return redirect('info')  # O donde tengas la URL de inicio de Info
    else:
        request.session['next'] = reverse('info')
        return redirect('/music/spotify-login')
