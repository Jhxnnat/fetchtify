from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import math
import requests

class Collage():
    def __init__(self, pallete=None, font=None):
        if pallete != None:
            self.pallete = pallete
        else:
            self.pallete = { # everforest 
                "bg": "#fffbef",
                "bg1": "#f2efdf",
                "bg2": "#e8e5d5",
                "bg3": "#dfdbc8",
                "bg4": "#d5d1bd",
                "bg5": "#c9c4b1",
                "fg": "#5c6a72",
                "fg1": "#687178",
                "fg2": "#747f84",
                "fg3": "#818c91",
                "fg4": "#8d989d",
                "red": "#f85552",
                "orange": "#f57d26",
                "yellow": "#dfa000",
                "green": "#8da101",
                "aqua": "#35a77c",
                "blue": "#3a94c5",
                "purple": "#df69ba",
                "black": "#5c6a72"
            }

        if font != None:
            self.font_large = ImageFont.truetype(font, 42)
            self.font_small = ImageFont.truetype(font, 32)
        else:
            self.font_large = ImageFont.truetype("../Agave", 42)
            self.font_small = ImageFont.truetype("../Agave", 32)

        self.gap = 10
        self.padding = 40
        self.collage_size = (700, 1010)

        (self.segment, self.header_height,
            self.image_height, self.footer_height) = self.layout(2,9,1)


    def generate(self, data, filename="collage.png", alt_header=None, alt_footer=None):
        self.collage = Image.new('RGB', self.collage_size, self.hex_to_rgb(self.pallete['bg']))
        draw = ImageDraw.Draw(self.collage)

        draw.rectangle(
            [(0, 0), (self.collage_size[0], self.header_height)],
            fill=self.hex_to_rgb(self.pallete['blue'])
        )
        draw.rectangle(
            [(0, self.collage_size[1]-self.footer_height), (self.collage_size[0], self.collage_size[1])],
            fill=self.hex_to_rgb(self.pallete['blue'])
        )

        #TODO: warp text - auto header text
        if alt_header == None:
            alt_header = "Your Stats"
        draw.text((self.padding, self.padding), alt_header, fill=self.pallete['fg'], font=self.font_large)

        x = self.padding
        y = self.header_height + self.padding
        data_len = len(data)
        _size = (self.image_height - (self.gap*(data_len-1)))
        size = _size // data_len
        for img, name, subname in data:
            # w = img['width']

            response = requests.get(img['url'])
            image = Image.open(BytesIO(response.content))
            cover = image.resize((size, size)) #images are squared anyways

            self.collage.paste(cover, (x, y))
            # draw.text((x + w + gap, y + (h//4)), name, fill=pallete['fg'], font=font_large)

            y += size + self.gap

        self.collage.save(filename)

    def hex_to_rgb(self, hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def layout(self, prop1, prop2, prop3):
        total = prop1 + prop2 + prop3
        segment = (self.collage_size[1] - self.padding*2) // total
        header_height = segment * prop1
        image_height = segment * prop2
        footer_height = segment * prop3
        return (segment, header_height, image_height, footer_height)
