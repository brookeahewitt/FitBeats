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


def search_for_track(token, track_name):
    url = url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = {"q": track_name, "type": "track", "limit": 1}

    result = get(url, headers=headers, params=query)
    json_result = json.loads(result.content)
    return json_result


def get_audio_features(token, track_id):
    url = f"https://api.spotify.com/v1/audio-features/{track_id}"
    headers = get_auth_header(token)

    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    return json_result


token = get_token()
song_info = search_for_track(token, "Stairway to Heaven")

track_id = song_info["tracks"]["items"][0]["id"]
audio_features = get_audio_features(token, track_id)
print(audio_features)
