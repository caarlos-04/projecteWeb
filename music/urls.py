from django.urls import path
from . import views

urlpatterns = [
    path('artist-selection/', views.artist_selection_view, name='artist_selection'),
    path('song-selection/', views.base_song_selection_view, name='base_song_selection'),
    path('discover/', views.discover_view, name='discover'),
    path('genres/', views.top_genres_view, name='genres'),
    path('spotify-login/', views.spotify_login, name='spotify_login'),

]