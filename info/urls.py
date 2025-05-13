from django.urls import path
from . import views

urlpatterns = [
    path('redirect',views.redirect_info, name='redirect_info' ),
    path('save-track/', views.save_track_to_playlist, name='save_track_to_playlist'),
    path('my-playlists/', views.user_playlists_view, name='user_playlists'),
    path('playlist/<int:playlist_id>/delete/', views.delete_playlist, name='delete_playlist'),
    path('playlist/<int:playlist_id>/remove/<int:track_id>/', views.remove_track_from_playlist,
         name='remove_track_from_playlist'),
    path('artist-info/', views.artist_info_view, name='artist_search'),
    path('top-songs-search/', views.top_songs_artist, name='top_songs_search'),

]