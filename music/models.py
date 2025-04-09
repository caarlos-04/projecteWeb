from django.db import models
from django.contrib.auth.models import User
from web.models import Artist

class UserArtistSelection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='artist_selections')
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    selected_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.artist.name}"