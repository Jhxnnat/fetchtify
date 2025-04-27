from blessings import Terminal

class Printing():
    def __init__(self, data_tracks, data_artist, config=None):
        self.config = config
        self.term = Terminal()
        self.data_tracks = data_tracks
        self.data_artist = data_artist
        self.header = '--- {t.bold}Fetchtify{t.normal} ---'.format(t=self.term)
        self.logo = config.ascii
        self.title = config.title

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
        lines_list = self.logo.split('\n')
        logo_lines_len = len(lines_list)
        _list = lines_list
        if info_len > logo_lines_len:
            _list = info

        t = self.term
        for i, logo in enumerate(_list):
            current_line  = ""
            if (i < logo_lines_len):
                current_line += lines_list[i] + '\t'
            if (i < info_len):
                current_line += info[i]
            print(current_line)

    def print(self, text):
        print(text.format(t=self.term))

