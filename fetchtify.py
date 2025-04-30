import os, sys, argparse, importlib
from modules.printing import Printing
from modules.spoty import Spoty

#TODO: config file documentation
class Config():
    def __init__(self):
        self.ascii = ""
        self.title = ""
        self.credentials_file = None
        self.defaults()
        self.SPOTIFY_CLIENT_ID = None
        self.SPOTIFY_CLIENT_SECRET = None

    def defaults(self):
        self.credentials_file = None
        self.title = "Fetchtify"
        self.ascii = """⠀⠀⠀⠀⠀⠀⠀⢀⣤⠖⠂⠉⠉⠉⠀⠒⠤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢀⠀⣶⡟⢀⣴⣶⣿⣾⣶⣶⣄⡀⠈⠑⢤⡀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⡴⣫⣼⡿⣴⡟⠛⠉⠉⠛⠛⠿⣿⣿⣷⣦⡀⠙⢄⠀⠀⠀⠀⠀⠀⠀
⠀⠀⣼⢁⣟⡟⣷⠁⠀⠀⠀⠀⠀⠀⠀⠀⠙⢿⣿⣷⣆⠈⢣⡀⠀⠀⠀⠀⠀
⠀⢰⣿⢼⣿⣷⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⣿⣿⡆⠀⢱⠀⠀⠀⠀⠀
⠀⢸⡵⣾⣇⣸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣧⠀⠀⢧⠀⠀⠀⠀
⠀⠘⣴⣿⢯⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⡿⠛⠉⠹⡆⠀⠀⠀
⢀⣼⣿⣧⠟⠁⢀⢀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢯⣴⣶⣴⡇⠀⠀⠀
⢸⣿⣼⣿⣋⣉⠀⠀⠀⠈⠙⠦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣿⣿⣷⣷⡀⠀⠀
⢸⠁⠊⣿⠛⢛⢟⣦⡀⠀⠀⠀⠈⢆⠀⠀⠀⠀⢀⠔⣨⣶⡜⠂⠈⠽⣧⡀⠀
⠸⣶⣾⡯⠤⢄⡀⠵⢿⣦⡀⠀⠀⠀⡷⡄⠀⡰⢁⣾⣿⣿⣿⠀⠀⠀⣿⡹⡄
⠀⣿⣡⠦⢄⡀⠈⠳⣬⣹⣿⣆⠀⠀⢉⠻⣴⠇⣾⣿⡟⢻⠁⠀⠀⠀⣿⠁⡇
⠀⣿⡭⡀⠀⠈⠲⣦⣸⣿⣿⣿⣧⣀⠈⡔⣜⣴⣿⡟⢀⡎⡈⠀⠀⢰⡿⢠⣷
⠀⢸⣿⣄⣒⡀⡀⣿⣷⡿⣿⢿⣿⣷⡰⡸⣯⣏⣿⡷⢋⣼⣁⡢⢠⠟⠀⣼⣿
⠀⠀⠻⣷⣈⣁⣮⢻⢸⡇⢨⣿⣿⣿⣷⢶⣿⣏⣩⣶⣿⣿⣿⣿⡯⣤⣴⣿⠃
⠀⠀⠀⠘⠿⣿⣿⣽⣽⣷⣿⣿⣿⣿⣿⡶⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠁⠀
⠀⠀⠀⠀⠀⠀⠉⠙⠿⢿⣿⣿⣿⣿⠟⠁⠀⠘⠿⣿⣿⣿⠿⠟⠉⠀⠀⠀⠀"""

    def usage(self):
        helpt = """
        Usage: fetchtify [ -h | -c config_file | -d | -n | -t title ]
          -h: show this message
          -c: provide configuration file
          -d: use the default configuration (overrides -c and -n)
          -n: do not show ascii text / logo
          -t: set custom title
        """
        print(helpt)
        os._exit(1)

    def get_config(self):
        parser = argparse.ArgumentParser(prog='fetchtify', description='neofetch-like tool for spotify')
        parser.add_argument('-c', '--config', help='provide a config file path')
        parser.add_argument('-d', '--default', action='store_true', help='use the default configuration (overrides other options)')
        parser.add_argument('-n', '--no_ascii', action='store_true', help='do not show ascii logo')
        parser.add_argument('-t', '--title', default="Fetchtify", help='provide a title')
        parser.add_argument('--credentials', help='provide a python file with spotify credentials (SPOTIFY_CLIENT_ID = <...>, SPOTIFY_CLIENT_SECRET = <...>)', required=True)

        args = parser.parse_args()
        self.title = args.title

        config = self.read_config_file(args.credentials)
        self.credentials_file = args.credentials
        if config['SPOTIFY_CLIENT_ID'] == None or config['SPOTIFY_CLIENT_SECRET'] == None:
            print("Invalid credentials")
            sys.exit(1)

        self.SPOTIFY_CLIENT_ID = config['SPOTIFY_CLIENT_ID']
        self.SPOTIFY_CLIENT_SECRET = config['SPOTIFY_CLIENT_SECRET']

        if args.no_ascii == True:
            self.ascii = ""

        if args.config != None:
            config = self.read_config_file(args.config)
            if config['title'] != None:
                self.title = config['title']
            if config['ascii'] != None:
                self.ascii = config['ascii']

        if args.default:
            self.defaults()

    def read_config_file(self, config_path):
        spec = importlib.util.spec_from_file_location("config_module", config_path)
        config_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(config_module)
        
        variables = {
            name: value 
            for name, value in vars(config_module).items() 
            if not name.startswith("__")
        }
        return variables

def main(config, credentials_file):
    if not os.path.isfile(credentials_file):
        print("ERROR: Invalid Environment File Path")
        os._exit(1)

    SPOTIFY_CLIENT_ID = config.SPOTIFY_CLIENT_ID
    SPOTIFY_CLIENT_SECRET = config.SPOTIFY_CLIENT_SECRET
    SPOTIFY_REDIRECT_URI = 'http://127.0.0.1:5000/callback/'
    
    if SPOTIFY_CLIENT_ID == None or SPOTIFY_CLIENT_SECRET == None:
        print("ERROR: Invalid Environment Variables")
        os._exit(1)


    scope='user-top-read user-read-recently-played user-library-read'
    term = "long_term"
    sp = Spoty(scope, term, SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI)
    sp.auth()
    tracks = sp.get_tracks()
    artist = sp.get_artist()
    p = Printing(data_tracks=tracks, data_artist=artist, config=config)
    p.show()


if __name__ == '__main__':
    config = Config()
    config.get_config()
    main(config, config.credentials_file)

