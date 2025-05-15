from django.contrib import admin
from .models import Artist, Track, Album, Playlist

admin.site.register(Artist)
admin.site.register(Track)
admin.site.register(Album)
admin.site.register(Playlist)