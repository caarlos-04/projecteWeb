import os
import requests
from django.shortcuts import redirect
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()

#Load environment variables
SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
SPOTIPY_REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI')


#Get session access token
def get_access_token(request):
    access_token = request.session.get('access_token')
    refresh_token = request.session.get('refresh_token')

    if not access_token:
        return None  #If there is no token the user needs to register

    #Check if the token is expired
    headers = {'Authorization': f'Bearer {access_token}'}
    test_response = requests.get('https://api.spotify.com/v1/me', headers=headers)

    if test_response.status_code == 401:  #Expired token
        if not refresh_token:
            return None

        new_token_info = refresh_access_token(refresh_token)
        if new_token_info:
            request.session['access_token'] = new_token_info['access_token']
            return new_token_info['access_token']
        else:
            return None

    return access_token


#Refres access token with the refresh token
def refresh_access_token(refresh_token):
    response = requests.post(
        'https://accounts.spotify.com/api/token',
        data={
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
            'client_id': SPOTIPY_CLIENT_ID,
            'client_secret': SPOTIPY_CLIENT_SECRET,
        }
    )
    if response.status_code == 200:
        return response.json()
    return None


#Request to the spotify api
def spotify_request(request, endpoint, params=None):
    access_token = get_access_token(request)
    if not access_token:
        return redirect('spotify_login')  #Redirect if no token

    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(f'https://api.spotify.com/v1/{endpoint}', headers=headers, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        return None

def refresh_access_token(session):
    refresh_token = session.get('refresh_token')
    client_id = os.getenv('SPOTIPY_CLIENT_ID')
    client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')

    payload = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': client_id,
        'client_secret': client_secret,
    }

    response = requests.post('https://accounts.spotify.com/api/token', data=payload)
    if response.status_code == 200:
        tokens = response.json()
        session['access_token'] = tokens['access_token']
        # Spotify puede o no devolver un nuevo refresh_token
        if 'refresh_token' in tokens:
            session['refresh_token'] = tokens['refresh_token']
        return True
    return False

def get_spotify_headers(request):
    access_token = request.session.get('access_token')
    refresh_token = request.session.get('refresh_token')

    # Si no hi ha access_token, no pots fer res
    if not access_token:
        raise Exception("No access token found")

    # Intenta fer una crida de prova
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get("https://api.spotify.com/v1/me", headers=headers)

    # Si el token ha expirat, refresca'l
    if response.status_code == 401:
        new_tokens = refresh_access_token(refresh_token)
        access_token = new_tokens['access_token']
        request.session['access_token'] = access_token
        headers["Authorization"] = f"Bearer {access_token}"

    return headers

