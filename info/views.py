from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from web.models import Artist, Album, Track, Playlist
import requests
from music.views import spotify_token_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST

@login_required
def redirect_info(request):
    access_token = request.session.get('access_token')

    if access_token:
        return redirect('info')
    else:
        request.session['next'] = reverse('info')
        return redirect('/music/spotify-login')

@login_required
@spotify_token_required
def artist_info_view(request):
    artist_name = request.GET.get('artist')
    artist_data = {}
    albums_data = []

    if artist_name:
        token = request.session.get('access_token')
        headers = {'Authorization': f'Bearer {token}'}

        # Buscar artista
        search_url = 'https://api.spotify.com/v1/search'
        params = {'q': artist_name, 'type': 'artist', 'limit': 15}
        search_resp = requests.get(search_url, headers=headers, params=params)

        if search_resp.status_code == 200:
            artists = search_resp.json().get('artists', {}).get('items', [])
            if artists:
                spotify_artist = artists[0]
                artist_data = {
                    'name': spotify_artist['name'],
                    'image': spotify_artist['images'][0]['url'] if spotify_artist['images'] else '',
                    'id': spotify_artist['id'],
                }

                # Buscar álbumes
                albums_url = f"https://api.spotify.com/v1/artists/{spotify_artist['id']}/albums"
                albums_resp = requests.get(albums_url, headers=headers, params={'include_groups': 'album', 'limit': 10})

                if albums_resp.status_code == 200:
                    for album in albums_resp.json().get('items', []):
                        album_data = {
                            'id': album['id'],
                            'title': album['name'],
                            'image': album['images'][0]['url'] if album['images'] else '',
                            'tracks': []
                        }

                        # Buscar tracks del álbum
                        tracks_url = f"https://api.spotify.com/v1/albums/{album['id']}/tracks"
                        tracks_resp = requests.get(tracks_url, headers=headers)
                        if tracks_resp.status_code == 200:
                            for track in tracks_resp.json().get('items', []):
                                album_data['tracks'].append({
                                    'title': track['name'],
                                    'id': track['id']
                                })

                        albums_data.append(album_data)

    context = {
        'artist': artist_data,
        'albums': albums_data,
        'playlists': Playlist.objects.filter(user=request.user)
    }

    return render(request, 'artist_info.html', context)

@csrf_exempt
@login_required
def save_track_to_playlist(request):
    if request.method == 'POST':
        track_title = request.POST['track_title']
        album_title = request.POST['album_title']
        artist_name = request.POST['artist_name']
        playlist_id = request.POST.get('playlist_id')
        new_playlist_title = request.POST.get('new_playlist_title')

        # Obtener o crear artist, album, track
        artist, _ = Artist.objects.get_or_create(name=artist_name)
        album, _ = Album.objects.get_or_create(title=album_title, artist=artist)
        track, _ = Track.objects.get_or_create(title=track_title, album=album, artist=artist)

        # Obtener o crear playlist
        if playlist_id:
            playlist = Playlist.objects.get(id=playlist_id)
        else:
            playlist, _ = Playlist.objects.get_or_create(title=new_playlist_title, user=request.user)

        playlist.tracks.add(track)

    next_url = request.POST.get('next', reverse('artist_search'))
    return redirect(next_url)

@login_required
def user_playlists_view(request):
    playlists = Playlist.objects.all()  # O solo del usuario si agregas relación
    return render(request, 'playlist.html', {'playlists': playlists})

@require_POST
def delete_playlist(request, playlist_id):
    playlist = get_object_or_404(Playlist, id=playlist_id)
    playlist.delete()
    return redirect('user_playlists')

@require_POST
def remove_track_from_playlist(request, playlist_id, track_id):
    playlist = get_object_or_404(Playlist, id=playlist_id)
    track = get_object_or_404(Track, id=track_id)
    playlist.tracks.remove(track)
    return redirect('user_playlists')

@login_required
@spotify_token_required
def top_songs_artist(request):
    artist_name = request.GET.get('artist')
    artist_data = {}
    songs_data = []

    if artist_name:
        token = request.session.get('access_token')
        headers = {'Authorization': f'Bearer {token}'}

        # Buscar artista
        search_url = 'https://api.spotify.com/v1/search'
        params = {'q': artist_name, 'type': 'artist', 'limit': 15}
        search_resp = requests.get(search_url, headers=headers, params=params)

        if search_resp.status_code == 200:
            artists = search_resp.json().get('artists', {}).get('items', [])
            if artists:
                spotify_artist = artists[0]
                artist_data = {
                    'name': spotify_artist['name'],
                    'image': spotify_artist['images'][0]['url'] if spotify_artist['images'] else '',
                    'id': spotify_artist['id'],
                }

                # Obtener canciones populares
                songs_url = f"https://api.spotify.com/v1/artists/{spotify_artist['id']}/top-tracks"
                songs_resp = requests.get(songs_url, headers=headers, params={'market': 'ES'})

                if songs_resp.status_code == 200:
                    for song in songs_resp.json().get('tracks', []):
                        song_data = {
                            'id': song['id'],
                            'title': song['name'],
                        }
                        songs_data.append(song_data)

    context = {
        'artist': artist_data,
        'songs': songs_data,
        'playlists': Playlist.objects.filter(user=request.user)
    }

    return render(request, 'artist_top_songs.html', context)