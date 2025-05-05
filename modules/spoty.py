import sys, webbrowser, requests, threading, time
import http.server
import socketserver
import urllib.parse
import base64
import datetime

auth_code = None

class Handler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass
    def do_GET(self):
        global auth_code
        if self.path.startswith('/callback'):
            query = urllib.parse.urlparse(self.path).query
            params = urllib.parse.parse_qs(query)
            auth_code = params.get('code', [None])[0]
            self.path = 'html/callback.html'
        else:
            self.send_error(404)
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

class Spoty():
    def __init__(self, scope, term, client_id, client_secret, redirect_uri):
        self.scope = scope
        self.term = term
        self.client_id=client_id
        self.client_secret=client_secret
        self.redirect_uri=redirect_uri
        
        self.auth_url = ""
        self.auth_code = None
        self.auth_token = None
        self.server = None
        self.thread = None

        self.access_token = None
        self.refresh_token = None

        self.limit = 5
        self.term = 'long_term'

    def make_auth_url(self):
        auth_url = f'https://accounts.spotify.com/authorize?client_id={self.client_id}&response_type=code&redirect_uri={self.redirect_uri}&scope={self.scope}'
        return auth_url
    
    def make_server(self, port):
        handler = Handler
        socketserver.TCPServer.allow_reuse_address = True
        self.server = socketserver.TCPServer(("", port), handler)
        self.thread = threading.Thread(target=self.server.serve_forever)
        self.thread.daemon = True
        try:
            self.thread.start()
        except KeyboardInterrupt:
            self.server.shutdown()
            sys.exit(1)

    def end_server(self):
        threading.Thread(target=self.server.shutdown, daemon=True).start()

    def is_access_token_expired(self):
        return false

    def auth(self):
        try:
            with open(".cache.access_token.txt", "r") as f:
                l = f.readline().strip()
                d = f.readline().strip()
                if int(d) + 3599 > int(datetime.datetime.now().strftime("%s")):
                    self.access_token = l
                    return
        except Exception as e:
            pass

        self.make_server(5000)

        auth_url = self.make_auth_url()
        webbrowser.open(auth_url)

        #FIXME: whats going on with "[2] Sandbox: CanCreateUserNamespace() clone() failure: EPERM"?
        while auth_code == None:
            pass

        self.access_token = self.get_access_token()
        self.end_server()

        d = datetime.datetime.now().strftime("%s")
        with open(".cache.access_token.txt", "w") as f:
            f.write(f"{self.access_token}")
            f.write("\n")
            f.write(f"{d}")

    def get_access_token(self):
        auth_str = f"{self.client_id}:{self.client_secret}"
        auth_bytes = auth_str.encode('utf-8')
        auth_base64 = base64.b64encode(auth_bytes).decode('utf-8')

        auth_url = 'https://accounts.spotify.com/api/token'
        headers = {
            'Authorization': 'Basic ' + auth_base64,
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = {
            'grant_type': 'authorization_code',
            'code': auth_code,
            'redirect_uri': self.redirect_uri
        }

        response = requests.post(auth_url, headers=headers, data=data)
        tokens = response.json()
        access_token = tokens['access_token']
        return access_token
    
    def current_user_top_artists(self, access_token, time_range = 'long_term', limit = 5):
        headers = {'Authorization': f'Bearer {access_token}'}
        params = {'time_range': time_range, 'limit': limit }
        response = requests.get('https://api.spotify.com/v1/me/top/artists', headers=headers, params=params)
        return response.json()

    def current_user_top_tracks(self, access_token, time_range = 'long_term', limit = 5):
        headers = {'Authorization': f'Bearer {access_token}'}
        params = {'time_range': time_range, 'limit': limit }
        response = requests.get('https://api.spotify.com/v1/me/top/tracks', headers=headers, params=params)
        return response.json()
    
    def get_artist(self):
        top_artists = self.current_user_top_artists(
            access_token=self.access_token,
            limit=self.limit, time_range=self.term)

        # print(top_artists)
        data = []
        for artist in top_artists['items']:
            data.append((artist['images'][0], artist['name'], ""))
        return data

    def get_tracks(self):
        top_tracks = self.current_user_top_tracks(
            access_token=self.access_token,
            limit=self.limit, time_range=self.term)

        data = []
        for track in top_tracks['items']:
            urls = track['album']['images'][0]
            artists = track['album']['artists']
            names = ""
            for artist in artists:
                names += f"{artist['name']} "
            data.append((urls, track['name'], names))
        return data


