import os
from modules.collage import Collage
from modules.stats import Stats
from modules.printing import Printing

stats = Stats()
tracks = stats.get_tracks()
artist = stats.get_artist()

# font_path = os.path.abspath("Iosevka.ttf") #TODO: verify this exists
# collage = Collage(font=font_path)
# collage.generate(tracks)

p = Printing(data_tracks=tracks, data_artist=artist)
p.show()

#TODO: cli arguments: show or not show some info, ascii, header
#TODO: config file?
#TODO: check if colors sequences are different on windows, if not, maybe we cant unuse blessings
