from django.db import models

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

class ListeningHistory(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='listening_history')
    track = models.ForeignKey(Track, on_delete=models.CASCADE)
    played_at = models.DateTimeField()

class Track(models.Model):
    title = models.CharField(max_length=100)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='tracks')
    album = models.ForeignKey(Album, on_delete=models.SET_NULL, null=True, blank=True, related_name='tracks')
    duration_ms = models.IntegerField()
    popularity = models.IntegerField(default=0)
    def __str__(self):
        return self.title

class SpotifyUser(models.Model):
    spotify_id = models.CharField(max_length=50, unique=True)
    display_name = models.CharField(max_length=100)
    profile_image = models.URLField(null=True, blank=True)
    def __str__(self):
        return self.display_name


# For more info on how to use Django model fields: 
# https://docs.djangoproject.com/en/stable/ref/models/fields/
