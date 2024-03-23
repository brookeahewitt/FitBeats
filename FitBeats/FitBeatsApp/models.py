from django.db import models

class Song(models.Model):
    song_name = models.CharField(max_length=200)
    artist_name = models.CharField(max_length=200)
    duration = models.DecimalField(max_digits=10)
    cover_art_link = models.URLField(max_length=400)
    preview_sound = models.URLField(max_length=400)


class Playlist(models.Model):
    songs = models.ManyToManyField(Song, related_name='songs_in_playlist', blank=True)

