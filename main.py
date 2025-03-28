import json
import os
import base64
import requests
from dotenv import load_dotenv
from requests import post
from flask import Flask

def create_flask(secret_key):
    app = Flask(__name__)
    app.secret_key = secret_key

def get_token(client_id, client_secret):
    auth_string = client_id  + ":" + client_secret
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

def get_current_track(token):
    auth_header = get_auth_header(token)
    url = "https://api.spotify.com/v1/me/player/currently-playing"
    response = requests.get(
        url,
        headers=auth_header
    )
    resp_json = response.json()
    print(resp_json)
    track_type = resp_json["currently_playing_type"]
    return track_type

def run():
    load_dotenv()
    secret_key = os.getenv("SECRET_KEY")
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    redirect_uri = "https://localhost:5000/callback"
    auth_url = "https://accounts.spotify.com/authorize"
    token_url = "https://accounts.spotify.com/api/token"
    api_base_url = "https://api.spotify.com/v1/"
    token = get_token(client_id, client_secret)
    print(token)
    print(get_current_track(token))

if __name__ == '__main__':
    run()
