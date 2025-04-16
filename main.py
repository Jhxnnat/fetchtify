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
    images.append((artist['images'][0], artist['name']))
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
import math

font_massive = ImageFont.truetype("Iosevka.ttf", 80)
font_large = ImageFont.truetype("Iosevka.ttf", 32)
font_small = ImageFont.truetype("Iosevka.ttf", 20)

_resize = 4
gap = 10
padding = 20
lpadding = padding * _resize
collage = Image.new('RGB', (700, 1400), (28, 28, 28))
draw = ImageDraw.Draw(collage)
draw.text((padding, padding), "Your Top Artists", fill="white", font=font_large)

x = padding * 8
y = padding * 8
i = 1
for img, name in images:
    w = img['width']//_resize
    h = img['height']//_resize
    response = requests.get(img['url'])
    _cover = Image.open(BytesIO(response.content))
    cover = _cover.resize((w, h))

    collage.paste(cover, (x, y))
    draw.text((lpadding, y + (h//4)), str(i), fill="white", font=font_massive)
    draw.text((x + w + gap, y + (h//4)), name, fill="white", font=font_large)
    i += 1

    y += padding + h + gap

collage.save('collage.png')
