import os
from modules.collage import Collage
from modules.stats import Stats

font_path = os.path.abspath("Agave.ttf") #TODO: verify this exists
stats = Stats()
collage = Collage(font=font_path)
# Collage(pallete, font)

# stats.show()
artist = stats.get_artist()
# tracks = stats.get_tracks()

# data = [
#     ("url", "name", "subname"),
#     ("url", "name", "subname")
#     ...
# ]

collage.generate(artist, alt_header="Favorite Songs")
# collage.generate(data, filename, header, footer)

