from django.db import models
from django.contrib.auth.models import User

class Artist(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Album(models.Model):
    title = models.CharField(max_length=100)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='albums')
    release_date = models.DateField(null=True, blank=True)
    def __str__(self):
        return self.title


class Track(models.Model):
    title = models.CharField(max_length=100)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='tracks')
    album = models.ForeignKey(Album, on_delete=models.SET_NULL, null=True, blank=True, related_name='tracks')
    duration_ms = models.IntegerField()
    popularity = models.IntegerField(default=0)
    def __str__(self):
        return self.title


class ListeningHistory(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='listening_history')
    track = models.ForeignKey(Track, on_delete=models.CASCADE)
    played_at = models.DateTimeField()

# For more info on how to use Django model fields: 
# https://docs.djangoproject.com/en/stable/ref/models/fields/

class UserArtistSelection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='artist_selections')
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='selected_by')
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.artist.name}"


