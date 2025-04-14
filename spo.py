from blessings import Terminal
t = Terminal()

import spotipy
from spotipy.oauth2 import SpotifyOAuth

import os
from dotenv import load_dotenv, dotenv_values
load_dotenv()
SPOTIFY_CLIENT_ID = os.getenv('CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('CLIENT_SECRET')
SPOTIFY_REDIRECT_URI = 'http://127.0.0.1:5000/callback/'

scope='user-top-read user-read-recently-played user-library-read'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope=scope
))

top_tracks = sp.current_user_top_tracks(limit=5)
top_artists = sp.current_user_top_artists(limit=5)

print(t.bold('This are your Spotify Stats!'))
print('{t.bold} Your Top {t.green} {t.underline} Artists{t.normal}:'.format(t=t))

print(top_artists)

# for idx, item in enumerate(top_artists['items']):
#     track = item['track']
#     print(idx, track['artists'][0]['name'], " – ", track['name'])

print('{t.bold} Your Top {t.green} {t.underline} Tracks{t.normal}:'.format(t=t))
print(top_tracks)


