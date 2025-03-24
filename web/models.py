from django.db import models

class Artist(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

# For more info on how to use Django model fields: 
# https://docs.djangoproject.com/en/stable/ref/models/fields/
