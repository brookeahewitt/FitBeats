import random

from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse

from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json
import logging

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

def generate_playlist(target_duration, max_iterations):
    playlist = []
    current_duration = 0
    iteration = 0

    while iteration < max_iterations:
        # Retrieve a batch of candidate tracks
        candidate_tracks = get_recommendations(token, ['pop'], 120, 140)
        random.shuffle(candidate_tracks)

        for track in candidate_tracks:
            if current_duration + track_duration_mins(track) <= target_duration + 1:
                playlist.append(track)
                current_duration += track_duration_mins(track)

        # Check if playlist duration is within acceptable range
        if target_duration - 1 <= current_duration <= target_duration + 1:
            break  # Exit loop if playlist duration is within acceptable range

        iteration += 1

    return playlist

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


# def index(request):
#     images_json = json.dumps(images)
#     return render(request, 'index.html', {'images': images_json, 'request': request})

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
    # images_json = json.dumps(images)
    return render(request, 'index.html', {'request': request})


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
        print("REQUEST",request)
        duration = request.POST.get('duration')
        print("DURATION:",duration)
        intensity = request.POST.get('intensity')
        print("INTENSITY", intensity)
        genre =  request.POST.get('selectedGenre')
        print("GENRE", genre)
        selected_exercises = request.POST.getlist('selectedExercises')
        print("SELECT EXERCISES", selected_exercises)
        selected_exercises_string = selected_exercises[0]  # Get the string from the list
        exercise_names = json.loads(selected_exercises_string)  # Parse the JSON string
        print(exercise_names)
        # Create a new playlist
        playlist = Playlist.objects.create(name="Custom Playlist")

        entire_workout = Entire_Workout.objects.create(
            playlist = playlist,
            duration = duration,
            intensity = intensity
        )

        for exercise_name in exercise_names:
            print(exercise_name)
            # Get or create the Exercise instance
            exercise, _ = Exercise.objects.get_or_create(
                exercise_name=exercise_name,
                entire_workout=entire_workout
            )

        # Redirect to a success page
        return HttpResponseRedirect(reverse('generate'))

        # If the request method is not POST, render the form again or return an appropriate response
    return render(request, 'generate.html')

