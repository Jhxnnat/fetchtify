# Fetchtify
neofetch-like tool for spotify.

# Dependencies:
- probably none.

# Usage:
fetchtify [-h] -c CONFIG [-d] [-n] [-t TITLE]

neofetch-like tool for spotify

options:
  -h, --help           show this help message and exit
  -c, --config CONFIG  provide a config file path ,Should containt at least SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET
  -d, --default        use the default configuration (overrides other options)
  -n, --no_ascii       do not show ascii logo
  -t, --title TITLE    provide a title

you should provide a python file with SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET, you can get these from: https://developer.spotify.com/dashboard
creating a new app with *WebAPI* as the scope (set the callback field to: http://localhost:5000/callback/ or http://127.0.0.1:5000/callback/).

