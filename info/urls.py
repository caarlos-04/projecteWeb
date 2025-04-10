from django.urls import path
from . import views

urlpatterns = [
    path('artist-info', views.info_artist_view, name='artist_info'),


]