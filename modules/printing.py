from blessings import Terminal

class Printing():
    def __init__(self, data_tracks, data_artist, config=None):
        self.config = config
        self.term = Terminal()
        self.data_tracks = data_tracks
        self.data_artist = data_artist
        self.ascii = config.ascii
        self.title = config.title
        self.header = '--- {t.bold}{self.title}{t.normal} ---'.format(t=self.term, self=self)

    # format the text that is going to be printed with the information, palette and so on
    def make_text_info(self): 
        t = self.term
        info = f'{self.header}\n\n'
        for item in self.data_tracks:
            title = item[1]
            subtitle = item[2]
            if len(subtitle) > 0:
                subtitle = ' - ' + subtitle
            info += f'{t.green}{title}{t.normal}{subtitle}'
            info += '\n'

        info += '\n'

        for item in self.data_artist:
            title = item[1]
            subtitle = item[2]
            if len(subtitle) > 0:
                subtitle = ' - ' + subtitle
            info += f'{t.green}{title}{t.normal}{subtitle}'
            info += '\n'

        info += '\n'
        # adding palette (nerd font required)
        info += f'󰝤 {t.red}󰝤 {t.orange}󰝤 {t.yellow}󰝤 {t.green}󰝤 {t.blue}󰝤 {t.cian}󰝤 {t.purple}{t.normal}'
        return info

    def show(self):
        info = self.make_text_info().split('\n')
        info_len = len(info)
        ascii_lines_list = self.ascii.split('\n')
        ascii_lines_len = len(ascii_lines_list)
        if info_len > ascii_lines_len:
            text = ""
            for i in range(len(ascii_lines_list[0])):
                text += " "
            for i in range(info_len - ascii_lines_len):
                ascii_lines_list.append(text)
        elif info_len < ascii_lines_len:
            text = ""
            for i in ascii_lines_list[0]:
                text += " "
            for i in range(ascii_lines_len - info_len):
                info.append(text)

        ascii_lines_len = len(ascii_lines_list)
        for i in range(ascii_lines_len):
            print(ascii_lines_list[i] + ' ' + info[i])

    def print(self, text):
        print(text.format(t=self.term))

