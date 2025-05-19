from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from web.models import Artist, Track
from .forms import ArtistSelectionForm
import os
import urllib.parse
from dotenv import load_dotenv, find_dotenv
import requests
from django.urls import reverse
from music.spotify_api import refresh_access_token
from music.spotify_api import get_spotify_headers

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

@login_required
def artist_selection_view(request):
    if 'access_token' not in request.session:
        request.session['next'] = request.path
        return redirect('spotify_login')
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
def spotify_login(request):
    client_id = os.getenv('SPOTIPY_CLIENT_ID')
    redirect_uri = os.getenv('SPOTIPY_REDIRECT_URI')
    scope = 'user-top-read user-read-private'
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
    client_id = os.getenv('SPOTIPY_CLIENT_ID')
    client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')
    redirect_uri = os.getenv('SPOTIPY_REDIRECT_URI')

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

@login_required
def get_top_artists(request):
    access_token = request.session.get('access_token')
    time_range = request.GET.get('time_range', 'medium_term')

    if not access_token:
        return JsonResponse({'error': 'No access token'}, status=401)

    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    url = 'https://api.spotify.com/v1/me/top/artists'
    params = {
        'limit': 10,
        'time_range': time_range,
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 401:

        if refresh_access_token(request.session):

            access_token = request.session.get('access_token')
            headers['Authorization'] = f'Bearer {access_token}'
            response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        return JsonResponse({
            'error': 'Spotify API error',
            'status': response.status_code,
            'response': response.json()
        }, status=response.status_code)

    data = response.json()
    artists_data = [
        {
            'name': artist['name'],
            'image': artist['images'][0]['url'] if artist['images'] else ''
        }
        for artist in data.get('items', [])
    ]

    return JsonResponse({'artists': artists_data})

@login_required
def get_top_songs(request):
    access_token = request.session.get('access_token')
    time_range = request.GET.get('time_range', 'medium_term')

    if not access_token:
        return JsonResponse({'error': 'No access token'}, status=401)

    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    url = 'https://api.spotify.com/v1/me/top/tracks'
    params = {
        'limit': 10,
        'time_range': time_range,
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 401:

        if refresh_access_token(request.session):

            access_token = request.session.get('access_token')
            headers['Authorization'] = f'Bearer {access_token}'
            response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        return JsonResponse({
            'error': 'Spotify API error',
            'status': response.status_code,
            'response': response.json()
        }, status=response.status_code)

    data = response.json()
    tracks_data = [
        {
            'name': track['name'],
            'image': track['album']['images'][0]['url'] if track['album']['images'] else ''
        }
        for track in data.get('items', [])
    ]

    return JsonResponse({'tracks': tracks_data})

def spotify_token_required(view_func):
    def wrapper(request, *args, **kwargs):
        access_token = request.session.get('access_token')
        refresh_token = request.session.get('refresh_token')

        if not access_token:
            if refresh_token:

                response = requests.post('https://accounts.spotify.com/api/token', data={
                    'grant_type': 'refresh_token',
                    'refresh_token': refresh_token,
                    'client_id': os.getenv('SPOTIFY_CLIENT_ID'),
                    'client_secret': os.getenv('SPOTIFY_CLIENT_SECRET'),
                })

                if response.status_code == 200:
                    data = response.json()
                    request.session['access_token'] = data['access_token']
                else:

                    request.session['next'] = request.path
                    return redirect(reverse('spotify_login'))
            else:

                request.session['next'] = request.path
                return redirect(reverse('spotify_login'))

        return view_func(request, *args, **kwargs)
    return wrapper

def recommendations(request):
    import logging
    import requests
    from django.http import JsonResponse

    time_range = request.GET.get('time_range', 'medium_term')
    fallback_ranges = ['medium_term', 'long_term', 'short_term']
    headers = get_spotify_headers(request)

    seed_track_ids = []
    seed_artist_ids = []

    try:
        # 🔹 PRIMER INTENT: obtenir top tracks
        for range_option in [time_range] + [r for r in fallback_ranges if r != time_range]:
            response = requests.get(
                f"https://api.spotify.com/v1/me/top/tracks?limit=5&time_range={range_option}",
                headers=headers
            )
            if response.status_code == 200:
                data = response.json()
                seed_track_ids = [track['id'] for track in data.get('items', [])]
                if seed_track_ids:
                    break  # Tenim tracks
            else:
                logging.warning(f"Top tracks failed: {response.status_code} {response.text}")

        # 🔹 SEGON INTENT: si no hi ha tracks, provem amb artistes
        if not seed_track_ids:
            for range_option in [time_range] + [r for r in fallback_ranges if r != time_range]:
                response = requests.get(
                    f"https://api.spotify.com/v1/me/top/artists?limit=5&time_range={range_option}",
                    headers=headers
                )
                if response.status_code == 200:
                    data = response.json()
                    seed_artist_ids = [artist['id'] for artist in data.get('items', [])]
                    if seed_artist_ids:
                        break
                else:
                    logging.warning(f"Top artists failed: {response.status_code} {response.text}")

        # 🔹 TERCER INTENT: si tampoc tenim artistes, fem servir valors per defecte
        if not seed_track_ids and not seed_artist_ids:
            # Aquestes seeds són públiques i segures
            seed_artist_ids = ['4NHQUGzhtTLFvgF5SZesLK']  # Tove Lo (exemple)
            seed_track_ids = ['0c6xIDDpzE81m2q797ordA']  # Royals de Lorde (exemple)

        # 🔹 Composar paràmetres segons el que tenim
        params = {
            'limit': 10,
            'market': 'ES',
        }
        if seed_track_ids:
            params['seed_tracks'] = ",".join(seed_track_ids[:5])
        if seed_artist_ids:
            params['seed_artists'] = ",".join(seed_artist_ids[:5])

        recs_response = requests.get(
            "https://api.spotify.com/v1/recommendations",
            headers=headers,
            params=params
        )

        if recs_response.status_code != 200:
            logging.error(f"Recommendations error: {recs_response.status_code} - {recs_response.text}")
            return JsonResponse({'recommendations': []})

        recs_data = recs_response.json()
        tracks = recs_data.get('tracks', [])

        recommendations = [{
            'name': track['name'],
            'artist': track['artists'][0]['name'],
            'image': track['album']['images'][0]['url'] if track['album']['images'] else '',
        } for track in tracks]


        return JsonResponse({'recommendations': recommendations})

    except Exception as e:
        logging.exception("Error obtenint recomanacions:")
        return JsonResponse({'recommendations': []})
