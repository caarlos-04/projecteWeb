from django.contrib import admin
from .models import Artist, ListeningHistory, Track, Album

admin.site.register(Artist)
admin.site.register(Track)
admin.site.register(ListeningHistory)
admin.site.register(Album)
