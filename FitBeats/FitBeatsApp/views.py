import random

from django.contrib.auth import logout
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json
import random

from .models import Playlist, Entire_Workout, Exercise, Song

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")


def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token


def get_auth_header(token):
    return {"Authorization": "Bearer " + token}


def generate_playlist(target_duration, max_iterations, token, genre):
    playlist = []
    current_duration = 0
    iteration = 0
    print("genre", genre)

    while iteration < max_iterations:
        # Retrieve a batch of candidate tracks
        candidate_tracks = get_recommendations(token, [genre], 120, 140)
        random.shuffle(candidate_tracks)

        for track in candidate_tracks:
            if track['preview_url']:
                if current_duration + track_duration_mins(track) <= target_duration + 1:
                    playlist.append(track)
                    current_duration += track_duration_mins(track)

        # Check if playlist duration is within acceptable range
        if target_duration - 1 <= current_duration <= target_duration + 1:
            break  # Exit loop if playlist duration is within acceptable range

        iteration += 1

    return playlist


def make_songs(playlist, playlist_name):
    song_list = []
    images = []
    created_playlist = Playlist.objects.create(name=playlist_name)
    for track in playlist:
        song_name = track["name"]
        duration = track["duration_ms"] / 60000
        images.append(track["album"]["images"][0]["url"])
        print(track['name'])
        song = Song.objects.create(
            song_name=song_name,
            duration=duration,
            cover_art_link=track["album"]["images"][0]["url"],
            artist_name=track["artists"][0]["name"],
            preview_sound=track['preview_url']
        )

        created_playlist.songs.add(song)
        song_list.append(song)

        images = images[:4]

    return song_list, created_playlist


def track_duration_mins(track):
    # Calculate the duration of the track
    return track["duration_ms"] / 60000


def get_recommendations(token, genres, min_tempo, max_tempo):
    url = "https://api.spotify.com/v1/recommendations"
    headers = get_auth_header(token)

    query = {
        "seed_genres": ",".join(genres),
        "min_tempo": min_tempo,
        "max_tempo": max_tempo,
        "min_popularity": 50,
        "available_markets": "US",
        "limit": 100,
    }

    result = get(url, headers=headers, params=query)
    json_result = json.loads(result.content)
    tracks = json_result["tracks"]
    return tracks


# token = get_token()
# playlist = generate_playlist(10, 10)
#
# images = []
#
# for track in playlist:
#     print(track["name"], track["duration_ms"])
#     images.append(track["album"]["images"][0]["url"])
#
# images = images[:4]


def index(request):
    playlists = Playlist.objects.filter(songs__isnull=False, songs__cover_art_link__isnull=False)

    for playlist in playlists:
        first_song = playlist.songs.first()
        if first_song:
            playlist.cover_image_url = first_song.cover_art_link

    return render(request, 'index.html', {'playlists': playlists})


# token = get_token()
# playlist = generate_playlist(10, 10)
#
# images = []
#
# for track in playlist:
#     print(track["name"], track["duration_ms"])
#     images.append(track["album"]["images"][0]["url"])
#
# images = images[:4]


def exercises(request):
    return render(request, 'exercises.html', {'request': request})


def generate(request):
    return render(request, 'generate.html', {'request': request})


def cardio(request):
    genre = request.GET.get('genre')
    print("Genre:", genre)  # Add this line for debugging
    return render(request, 'cardio.html', {'genre': genre})


def weight_lifting(request):
    genre = request.GET.get('genre')
    return render(request, 'weight_lifting.html', {'genre': genre})


def pilates(request):
    genre = request.GET.get('genre')
    return render(request, 'pilates.html', {'genre': genre})


def yoga(request):
    genre = request.GET.get('genre')
    return render(request, 'yoga.html', {'genre': genre})


def calisthenics(request):
    genre = request.GET.get('genre')
    return render(request, 'calisthenics.html', {'genre': genre})


def stretching(request):
    genre = request.GET.get('genre')
    return render(request, 'stretching.html', {'genre': genre})


def info(request):
    return render(request, 'info.html', {'request': request})


def logout_view(request):
    logout(request)
    return redirect('index')


def completeWorkout(request):
    return render(request, 'completeWorkout.html', {'request': request})


def submit_workout(request):
    if request.method == 'POST':
        # Process the form data
        duration = request.POST.get('duration')
        intensity = request.POST.get('intensity')
        genre = request.POST.get('selectedGenre')
        playlist_name = request.POST.get('playlist_name')
        print("PLAYLIST NAME:", playlist_name)
        num_breaks = int(request.POST.get('num_breaks'))
        selected_exercises = request.POST.getlist('selectedExercises')
        selected_exercises_string = selected_exercises[0]  # Get the string from the list
        exercise_names = json.loads(selected_exercises_string)  # Parse the JSON string
        # Create a new playlist
        token = get_token()
        playlist = generate_playlist(int(duration), 10, token, genre)  # Adjust parameters as needed
        songs, created_playlist = make_songs(playlist, playlist_name)

        entire_workout = Entire_Workout.objects.create(
            playlist=created_playlist,
            duration=duration,
            intensity=intensity,
            exerciser=request.user
        )

        val = 1
        if num_breaks > 0:
            for i in range(num_breaks):
                random_num = random.randint(1, len(exercise_names) - 1)
                exercise_names.insert(random_num, "Break " + str(val))
                val += 1

        exercise_names.insert(0, "Warm Up")
        exercise_names.append("Cool Down")

        for exercise_name in exercise_names:
            # Get or create the Exercise instance
            exercise, _ = Exercise.objects.get_or_create(
                exercise_name=exercise_name,
                entire_workout=entire_workout
            )

        total_duration = sum(song.duration for song in created_playlist.songs.all()) if playlist else 0

        return render(request, 'completeWorkout.html',
                      {'workout': entire_workout, 'exercises': exercise_names, 'playlist': entire_workout.playlist,
                       'entire_duration': total_duration})

        # If the request method is not POST, render the form again or return an appropriate response
    return render(request, 'generate.html')


def playlist_detail(request):
    # Retrieve the playlist object from the database
    if request.method == 'POST':
        playlist_id = request.POST.get("playlist_id")

        playlist = get_object_or_404(Playlist, id=int(playlist_id))

        entire_workout = Entire_Workout.objects.filter(playlist=playlist).first()

        print(entire_workout)
        total_duration = entire_workout.duration
        exercise_names = list(entire_workout.exercise_set.values_list('exercise_name', flat=True))

        # Pass the playlist object to the template
        return render(request, 'completeWorkout.html',
                      {'workout': entire_workout, 'exercises': exercise_names, 'playlist': entire_workout.playlist,
                       'entire_duration': total_duration})


def activity(request):
    playlists = Playlist.objects.filter(songs__isnull=False, songs__cover_art_link__isnull=False)

    for playlist in playlists:
        first_song = playlist.songs.first()
        if first_song:
            playlist.cover_image_url = first_song.cover_art_link

    return render(request, 'activity.html', {'playlists': playlists})
