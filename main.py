# Desktop App for now

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import os
from googleapiclient.errors import HttpError
import time
import re

from dotenv import load_dotenv

# Get ENV variables
load_dotenv()

# Setup Spotify API Credentials
SPOTIPY_CLIENT_ID = os.getenv('CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('CLIENT_SECRET')
SPOTIPY_REDIRECT_URI = 'http://localhost:8888/callback'
SPOTIFY_SCOPE = 'playlist-read-private'

# Set up YouTube API credentials, forcing SSL (privacy and integrity)
YOUTUBE_SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]

def auth_spotify():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI,
        scope=SPOTIFY_SCOPE
    ))
    return sp

def auth_youtube():
    creds = None
    # load creds from credential file
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", YOUTUBE_SCOPES)
    
    # if no valid creds avail, prompt user to login
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", YOUTUBE_SCOPES
            )
            # check which port to run on
            creds = flow.run_local_server(port=0)
        
        # save creds for future use
        with open("credentials.json", "w") as token:
            token.write(creds.to_json())

    youtube = build("youtube", "v3", credentials=creds)
    return youtube

def get_spotify_playlist_tracks(sp, playlist_id):
    tracks = []
    results = sp.playlist_tracks(playlist_id)
    tracks.extend(results['items'])
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])   
    return tracks

def create_yt_playlist(yt, title, descr):
    req = yt.playlists().insert(
        part="snippet, status",
        body={
            "snippet": {
                "title": title,
                "description": descr
            },
            "status": {
                "privacyStatus": "private"
            }
        }
    )
    res = req.execute()
    return res["id"]

def search_yt_video(yt, query):
    req = yt.search().list(
        part="snippet",
        maxResults=1,
        q=query
    )
    res = req.execute()
    # get and return first result
    if res["items"]:
        return res["items"][0]["id"]["videoId"]
    return None

def add_vid_to_playlist(yt, playlist_id, video_id):
    max_retries = 3
    delay = 5  # seconds

    for attempt in range(max_retries):
        try:
            req = yt.playlistItems().insert(
                part="snippet",
                body={
                    "snippet": {
                        "playlistId": playlist_id,
                        "resourceId": {
                            "kind": "youtube#video",
                            "videoId": video_id
                        }
                    }
                }
            )
            response = req.execute()
            print("Video added successfully:", response)
            return response  # Exit after a successful request
        except HttpError as e:
            if e.resp.status == 409:  # Specific error status for retry logic
                print(f"Attempt {attempt + 1} failed: {e}")
                time.sleep(delay)
            else:
                print(f"An unexpected error occurred: {e}")
                raise  # Re-raise unexpected errors
    raise Exception("Max retries exceeded")

def transfer_playlist(url, yt_playlist_title):
    
    spotify_playlist_id = parse_spotify_playlist_url(url)
    
    # auth spotify
    sp = auth_spotify()

    # auth yt
    yt = auth_youtube()

    # get spotify trakcs for that playlist
    tracks = get_spotify_playlist_tracks(sp, spotify_playlist_id)

    # create yt playlist
    yt_playlist_id = create_yt_playlist(yt, yt_playlist_title, "From Spotify")

    # search each track on yt and add it to new playlist
    for track in tracks:
        track_name = track['track']['name']
        artist_name = track['track']['artists'][0]['name']
        query = f"{track_name} {artist_name}"
        # look for the video and get id of first video
        video_id = search_yt_video(yt, query)
        if video_id:
            add_vid_to_playlist(yt, yt_playlist_id, video_id)
            print(f"Added {track_name} by {artist_name} to YouTube playlist")
        else:
            print(f"Could not find {track_name} by {artist_name} on YouTube")

def parse_spotify_playlist_url(url):
    pattern = r"playlist/([^?]+)"
    match = re.search(pattern, url)
    if match:
        playlist_id = match.group(1)
        return playlist_id
    else:
        raise Exception("Oops! Enter a valid Spotify playlist URL.")

if __name__ == "__main__":
    spotify_playlist_id = 'https://open.spotify.com/playlist/37i9dQZF1DX9tPFwDMOaN1?si=03ab893f64954f7c'
    youtube_playlist_title = 'KPOP ON'
    transfer_playlist(spotify_playlist_id, youtube_playlist_title)

    # https://open.spotify.com/playlist/37i9dQZF1DX9tPFwDMOaN1?si=03ab893f64954f7c