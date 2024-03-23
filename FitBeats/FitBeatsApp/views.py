import random
from django.shortcuts import render

from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json

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




token = get_token()
playlist = generate_playlist(10, 10)

for track in playlist:
    print(track["name"], track["duration_ms"])



def index(request):
    return render(request, 'index.html')


def exercises(request):
    return render(request, 'exercises.html')


def generate(request):
    return render(request, 'generate.html')
