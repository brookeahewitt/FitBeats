from django.db import models

class Song(models.Model):
    song_name = models.CharField(max_length=200)
    artist_name = models.CharField(max_length=200)
    duration = models.DecimalField(max_digits=10, decimal_places=2)
    cover_art_link = models.URLField(max_length=400)
    preview_sound = models.URLField(max_length=400)


class Playlist(models.Model):
    songs = models.ManyToManyField(Song, related_name='songs_in_playlist', blank=True)
    cover_image = models.URLField(max_length=400)
    name = models.CharField(max_length=200)


class Entire_Workout(models.Model):
    # segments = models.ForeignKey(Workout_Segment, on_delete=models.CASCADE)
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE, null=True)
    duration = models.DecimalField(decimal_places=2, max_digits=10)
    intensity = models.DecimalField(decimal_places=2, max_digits=10)


class Exercise(models.Model):
    exercise_name = models.CharField(max_length=200)
    entire_workout = models.ForeignKey(Entire_Workout, on_delete=models.CASCADE)

# class Workout_Segment(models.Model):
#     exercise_names = models.ManyToManyField(Exercise, related_name="exercises", blank=True)
#     workout_type = models.CharField(max_length=200)
#     duration = models.DecimalField(decimal_places=2, max_digits=10)
#     intensity = models.DecimalField(decimal_places=2, max_digits=10)

