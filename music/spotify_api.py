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
