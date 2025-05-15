from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from music.spotify_api import refresh_access_token
from web.models import Artist, Album, Track, Playlist
import requests
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST

@login_required
def redirect_info(request):
    access_token = request.session.get('access_token')

    if access_token:
        return redirect('info')
    else:
        request.session['next'] = reverse('info')
        return redirect('/music/spotify-login')

def _make_spotify_request(url, request, params=None):
    """
    Helper to make authenticated Spotify requests and refresh token on 401
    """
    token = request.session.get('access_token')
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 401:
        if refresh_access_token(request.session):
            token = request.session.get('access_token')
            headers['Authorization'] = f'Bearer {token}'
            response = requests.get(url, headers=headers, params=params)

    return response

@login_required
def artist_info_view(request):
    artist_name = request.GET.get('artist')
    artist_data = {}
    albums_data = []

    if artist_name:
        params = {'q': artist_name, 'type': 'artist', 'limit': 15}
        search_resp = _make_spotify_request('https://api.spotify.com/v1/search', request, params=params)

        if search_resp.status_code == 200:
            artists = search_resp.json().get('artists', {}).get('items', [])
            if artists:
                spotify_artist = artists[0]
                artist_data = {
                    'name': spotify_artist['name'],
                    'image': spotify_artist['images'][0]['url'] if spotify_artist['images'] else '',
                    'id': spotify_artist['id'],
                }

                albums_url = f"https://api.spotify.com/v1/artists/{spotify_artist['id']}/albums"
                albums_resp = _make_spotify_request(albums_url, request, params={'include_groups': 'album', 'limit': 10})

                if albums_resp.status_code == 200:
                    for album in albums_resp.json().get('items', []):
                        album_data = {
                            'id': album['id'],
                            'title': album['name'],
                            'image': album['images'][0]['url'] if album['images'] else '',
                            'tracks': []
                        }

                        tracks_url = f"https://api.spotify.com/v1/albums/{album['id']}/tracks"
                        tracks_resp = _make_spotify_request(tracks_url, request)

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

@require_POST
@login_required
def save_track_to_playlist(request):
    track_title = request.POST['track_title']
    album_title = request.POST['album_title']
    artist_name = request.POST['artist_name']
    playlist_id = request.POST.get('playlist_id')
    new_playlist_title = request.POST.get('new_playlisttitle')

    artist,  = Artist.objects.get_or_create(name=artist_name)
    album,  = Album.objects.get_or_create(title=album_title, artist=artist)
    track,  = Track.objects.get_or_create(title=track_title, album=album, artist=artist)

    if playlist_id:
        playlist = Playlist.objects.get(id=playlist_id, user=request.user)
    else:
        playlist,  = Playlist.objects.get_or_create(title=new_playlist_title, user=request.user)

    playlist.tracks.add(track)

    return JsonResponse({'success': True, 'message': f'"{track.title}" saved to "{playlist.title}"'})

@login_required
def user_playlists_view(request):
    playlists = Playlist.objects.filter(user=request.user)
    return render(request, 'playlist.html', {'playlists': playlists})

@require_POST
def delete_playlist(request, playlist_id):
    playlist = get_object_or_404(Playlist, id=playlist_id, user=request.user)

    for track in playlist.tracks.all():
        playlist.tracks.remove(track)

        if not check_track_in_other_playlists(track, playlist):
            if not check_album_songs_left(track.album):
                track.album.delete()
            if not check_artist_songs_left(track.artist):
                track.artist.delete()
            track.delete()

    playlist.delete()
    return redirect('user_playlists')

def check_album_songs_left(album):
    return Playlist.objects.filter(tracks__album=album).exists()

def check_artist_songs_left(artist):
    return Playlist.objects.filter(tracks__artist=artist).exists()

def check_track_in_other_playlists(track, current_playlist):
    return Playlist.objects.filter(tracks=track).exclude(id=current_playlist.id).exists()

@require_POST
def remove_track_from_playlist(request, playlist_id, track_id):
    playlist = get_object_or_404(Playlist, id=playlist_id, user=request.user)
    track = get_object_or_404(Track, id=track_id)

    playlist.tracks.remove(track)

    if not check_track_in_other_playlists(track, playlist):
        if not check_artist_songs_left(track.artist):
            track.artist.delete()
        if not check_album_songs_left(track.album):
            track.album.delete()
        track.delete()
    return redirect('user_playlists')

@login_required
def top_songs_artist(request):
    artist_name = request.GET.get('artist')
    artist_data = {}
    songs_data = []
    if artist_name:
        params = {'q': artist_name, 'type': 'artist', 'limit': 15}
        search_resp = _make_spotify_request('https://api.spotify.com/v1/search', request, params=params)

        if search_resp.status_code == 200:
            artists = search_resp.json().get('artists', {}).get('items', [])
            if artists:
                spotify_artist = artists[0]
                artist_data = {
                    'name': spotify_artist['name'],
                    'image': spotify_artist['images'][0]['url'] if spotify_artist['images'] else '',
                    'id': spotify_artist['id'],
                }

                songs_url = f"https://api.spotify.com/v1/artists/{spotify_artist['id']}/top-tracks"
                songs_resp = _make_spotify_request(songs_url, request, params={'market': 'ES'})

                if songs_resp.status_code == 200:
                    for song in songs_resp.json().get('tracks', []):
                        songs_data.append({
                            'id': song['id'],
                            'title': song['name'],
                            'album': song['album']['name'],
                        })

    context = {
        'artist': artist_data,
        'songs': songs_data,
        'playlists': Playlist.objects.filter(user=request.user)
    }

    return render(request, 'artist_top_songs.html', context)