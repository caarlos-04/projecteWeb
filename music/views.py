from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from web.models import Artist, Track
from .forms import ArtistSelectionForm
import os
import urllib.parse
from dotenv import load_dotenv
import requests
from django.urls import reverse

load_dotenv()

@login_required
def artist_selection_view(request):
    form = ArtistSelectionForm(request.POST or None)
    if request.method == "POST" and form.is_valid():

        selected_artist = form.cleaned_data['artist']

        return redirect('song_selection', artist_id=selected_artist.id)
    context = {
        'form': form,
        'artists': Artist.objects.all()
    }
    return render(request, 'artist_selection.html', context)

@login_required
def song_selection_view(request, artist_id, song_id):
    artist = get_object_or_404(Artist, id=artist_id)
    song_id = get_object_or_404(Track, id=song_id)

    context = {'artist': artist, 'song': song_id}
    return render(request, 'song_selection.html', context)

@login_required
def base_song_selection_view(request):
    return render(request, 'song_selection.html')

@login_required
def discover_view(request):
    return render(request, 'discover.html')

@login_required
def top_genres_view(request):
    return render(request, 'genres.html')

@login_required
def spotify_login(request):
    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    redirect_uri = os.getenv('SPOTIFY_REDIRECT_URI')
    scope = 'user-top-read user-read-private'  # Ajusta los permisos que necesites

    params = {
        'client_id': client_id,
        'response_type': 'code',
        'redirect_uri': redirect_uri,
        'scope': scope,
    }

    url = 'https://accounts.spotify.com/authorize?' + urllib.parse.urlencode(params)
    return redirect(url)

@login_required
def spotify_callback(request):
    code = request.GET.get('code')
    if not code:
        return redirect('home')
    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
    redirect_uri = os.getenv('SPOTIFY_REDIRECT_URI')

    payload = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': redirect_uri,
        'client_id': client_id,
        'client_secret': client_secret,
    }

    response = requests.post('https://accounts.spotify.com/api/token', data=payload)
    response_data = response.json()

    access_token = response_data.get('access_token')
    refresh_token = response_data.get('refresh_token')

    # Guardar en sesión
    request.session['access_token'] = access_token
    request.session['refresh_token'] = refresh_token

    # Redirigir a donde el usuario quería ir
    next_url = request.session.pop('next', '/')
    return redirect(next_url)

@login_required
def redirect_music(request):
    access_token = request.session.get('access_token')

    if access_token:
        return redirect('music')  # O donde tengas la URL de inicio de Music
    else:
        # Guardamos a dónde quería ir
        request.session['next'] = reverse('music')
        return redirect('/music/spotify-login')