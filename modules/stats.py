import spotipy
from spotipy.oauth2 import SpotifyOAuth

class Stats():
    def __init__(self, SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI):
        self.scope='user-top-read user-read-recently-played user-library-read'
        self.term = "long_term"
        self.limit = 5
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=SPOTIFY_CLIENT_ID,
            client_secret=SPOTIFY_CLIENT_SECRET,
            redirect_uri=SPOTIFY_REDIRECT_URI,
            scope=self.scope
        ))
        self.top_artists = None
        self.top_tracks = None

    def get_artist(self):
        self.top_artists = self.sp.current_user_top_artists(
            limit=self.limit, time_range=self.term
        )
        data = []
        for artist in self.top_artists['items']:
            data.append((artist['images'][0], artist['name'], ""))
        return data

    def get_tracks(self):
        self.top_tracks = self.sp.current_user_top_tracks(
            limit=self.limit, time_range=self.term
        )

        data = []
        for track in self.top_tracks['items']:
            urls = track['album']['images'][0]
            artists = track['album']['artists']
            names = ""
            for artist in artists:
                names += f"{artist['name']} "
            data.append((urls, track['name'], names))
        return data

