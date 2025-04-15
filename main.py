import requests
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

term = "long_term"
limit = 5
top_tracks = sp.current_user_top_tracks(limit=limit, time_range=term)
top_artists = sp.current_user_top_artists(limit=limit, time_range=term)

print(t.bold('These are your Spotify Stats!\n'))
print('{t.bold} Your Top {t.green}{t.underline}Artists{t.normal}:\n'.format(t=t))

images = []

i = 1
for artist in top_artists['items']:
    print(f"\t{i}. {artist['name']}")
    images.append(artist['images'][0])
    i += 1

print()
print('{t.bold} Your Top {t.green}{t.underline}Tracks{t.normal}:\n'.format(t=t))

i = 1
for track in top_tracks['items']:
    artists = track['album']['artists']
    names = ""
    for artist in artists:
        names += f"{artist['name']} "
    print(f"\t{i}. {track['name']} - {names}")
    i += 1

print()

from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

for img in images:
    response = requests.get(img['url'])
    w = img['width']
    h = img['height']

    # _image = Image.new('RGB', (w, h), (28, 28, 28))
    _image = Image.open(BytesIO(response.content))

    draw = ImageDraw.Draw(_image)

    font_large = ImageFont.truetype("Iosevka.ttf", 32)
    font_small = ImageFont.truetype("Iosevka.ttf", 20)

    draw.text((50, 50), "Some test", fill="white", font=font_large)
    draw.text((50, 120), "Some text", fill="white", font=font_small)
    draw.text((50, 160), "1234...", fill="white", font=font_small)

    _image.save('test.png')

    break
