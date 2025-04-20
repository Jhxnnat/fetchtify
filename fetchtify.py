import os
from modules.collage import Collage
from modules.stats import Stats

font_path = os.path.abspath("Iosevka.ttf") #TODO: verify this exists
stats = Stats()

collage = Collage(font=font_path)

# artist = stats.get_artist()
tracks = stats.get_tracks()

collage.generate(tracks)

