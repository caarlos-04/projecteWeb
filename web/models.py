from django.db import models
from django.contrib.auth.models import User

class Artist(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Album(models.Model):
    title = models.CharField(max_length=100)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='albums')
    def __str__(self):
        return self.title


class Track(models.Model):
    title = models.CharField(max_length=100)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='tracks')
    album = models.ForeignKey(Album, on_delete=models.SET_NULL, null=True, blank=True, related_name='tracks')
    image = models.ImageField()
    def __str__(self):
        return self.title


class Playlist(models.Model):
    title = models.CharField(max_length=100)
    tracks = models.ManyToManyField('Track', blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='playlists')

    def __str__(self):
        return self.title

# For more info on how to use Django model fields:
# https://docs.djangoproject.com/en/stable/ref/models/fields/

