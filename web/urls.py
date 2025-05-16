from django.urls import path, include
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views
from . import views
from info import views as info_views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('about_us/', views.about_us_view, name='about_us'),
    path('music/', views.base_music_view, name='music'),
    path('info/', views.base_info_view, name='info'),
    path('playlists/', info_views.user_playlists_view, name='playlists'),
    path('music-info/', info_views.artist_info_view, name='music_info'),
    path('top-songs/', info_views.top_songs_artist, name='top_songs'),
    path('spotify/login/', info_views.redirect_info, name='spotify_login'),
] 