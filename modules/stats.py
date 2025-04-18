import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv, dotenv_values

class Stats():
    def __init__(self):
        load_dotenv()
        SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
        SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
        SPOTIFY_REDIRECT_URI = 'http://127.0.0.1:5000/callback/'

        self.scope='user-top-read user-read-recently-played user-library-read'
        self.term = "long_term"
        self.limit = 5
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=SPOTIFY_CLIENT_ID,
            client_secret=SPOTIFY_CLIENT_SECRET,
            redirect_uri=SPOTIFY_REDIRECT_URI,
            scope=self.scope
        ))

    def get_artist(self):
        top_artists = self.sp.current_user_top_artists(
            limit=self.limit, time_range=self.term
        )
        data = []
        for artist in top_artists['items']:
            data.append((artist['images'][0], artist['name'], ""))
        return data

    def get_tracks(self):
        top_tracks = self.sp.current_user_top_tracks(
            limit=self.limit, time_range=self.term
        )

        data = []
        for track in top_tracks['items']:
            urls = ""
            artists = track['album']['artists']
            names = ""
            for artist in artists:
                names += f"{artist['name']} "
            data.append((urls, track['name'], names))
        return data

