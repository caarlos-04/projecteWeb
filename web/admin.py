from django.contrib import admin
from .models import Artist, Track, Album, Playlist


# Admin bàsic per Artist, Track i Album
admin.site.register(Artist)
admin.site.register(Track)
admin.site.register(Album)

# Admin personalitzat per Playlist
@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ('title', 'user')
    filter_horizontal = ('tracks',)