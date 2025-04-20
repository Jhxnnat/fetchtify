from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import math
import requests

class Collage():
    def __init__(self, palette=None, font=None):
        if palette != None:
            self.palette = palette
        else:
            self.palette = {
                "bg": "#fff4e6",        # Soft peach cream
                "bg1": "#f5e9dd",       # Warm antique white
                "bg2": "#ebdfd2",       # Soft beige
                "bg3": "#e0d4c4",       # Warm parchment
                "bg4": "#d6c9b7",       # Toasted almond
                "bg5": "#ccbda8",       # Warm gray-beige
                
                "fg": "#654b3a",       # Coffee brown
                "fg1": "#756050",       # Warm taupe
                "fg2": "#857565",       # Muted clay
                "fg3": "#958a7a",       # Warm stone
                "fg4": "#a59e8f",       # Soft khaki
                
                "red": "#e56b55",       # Terracotta red
                "orange": "#e68a3e",     # Pumpkin spice
                "yellow": "#d18d00",     # Mustard gold
                "green": "#7d8c40",      # Olive green
                "aqua": "#3d8e7c",       # Teal (slightly warmer)
                "blue": "#3a7a96",       # Denim blue (muted)
                "purple": "#c975a6",     # Dusty lavender
                "black": "#543e2e"       # Dark chocolate
            }

        if font != None:
            self.font_large = ImageFont.truetype(font, 42)
            self.font_small = ImageFont.truetype(font, 32)
        else:
            self.font_large = ImageFont.truetype("../Agave", 42)
            self.font_small = ImageFont.truetype("../Agave", 32)

        self.gap = 10
        self.padding = 40
        self.collage_size = [0, 0]
        self.middle_hori = 0
        self.middle_vert = 0
        self.palette_height = 0
        self.info_height = 0
        self.header_height = 0

    def generate(self, data, filename="collage.png"):
        img = data[0][0]
        response = requests.get(img['url'])
        image = Image.open(BytesIO(response.content))
        print(image.palette)
        # TODO: get palette from image

        self.collage_size = [img['width'] * 2, img['height']]
        self.calculate_layout()

        image_size = (self.collage_size[0], self.collage_size[1])
        self.collage = Image.new('RGB', image_size, self.hex_to_rgb("#282828"))
        self.collage.paste(image, (0, 0))

        draw = ImageDraw.Draw(self.collage)
        self.draw_palette(draw)

        self.collage.save(filename)

    def hex_to_rgb(self, hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def calculate_layout(self):
        self.middle_hori = self.collage_size[0] // 2
        self.middle_vert = self.collage_size[1] // 2
        self.palette_height = self.middle_vert // 5
        self.header_height = self.info_height // 5
        self.info_height = (self.collage_size[1] - self.palette_height - self.header_height)
        return None
    
    def draw_palette(self, draw, colors=["red", "orange", "yellow", "green", "aqua", "blue", "purple"]):
        y = self.collage_size[1] - self.palette_height
        amount = len(colors)
        cell_size = self.middle_hori // amount
        x1, x2 = self.middle_hori, self.middle_hori + cell_size
        for i, color in enumerate(colors):
            draw.rectangle(
                [(x1, y), (x2, self.collage_size[1])],
                fill=self.hex_to_rgb(self.palette[color])
            )
            x1 += cell_size+1
            x2 += cell_size+1
