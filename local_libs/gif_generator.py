from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import unicodedata


# 根据文本创建gif
class GIFGenerator:
    def __init__(self, fg_color=(0, 0, 0), bg_color=(255, 255, 255)):
        self.SELECTOR = '\ufe0f'    # emoji selector
        self.canvas_height = 1024
        self.canvas_width = 1024
        self.max_cols = 10
        self.max_rows = 10
        self.max_chars = 100
        self.font_file = 'simhei'
        # self.fontsize = 56
        self.fontsize = 96
        self.fg_color = fg_color
        self.bg_color = bg_color
        # self.font_file = 'resources/fonts/EmojiOneColor-SVGinOT.ttf'

    def set_fg(self, color_str):
        self.fg_color = '#' + color_str

    def set_bg(self, color_str):
        self.bg_color = '#' + color_str

    def parse(self, txt):   # return parsed text with \n added
        output = ""
        current_row = 1
        current_col = 0     # width already occupied
        char_count = 0

        for ch in txt:
            # what will happen AFTER ch is appended (not yet
            if unicodedata.east_asian_width(ch) in ['W', 'F', 'A']:
                current_width = 1
            else:
                current_width = 0.5

            if ch == '\n':
                current_row += 1
                current_col = 0
            elif ch == self.SELECTOR:
                continue
            else:
                current_col += current_width

            if current_col > self.max_cols:
                output += '\n'
                char_count += 1
                current_row += 1
                current_col = current_width
            else:
                pass

            if current_row > self.max_rows:
                print('Warning: canvas full. String may be trimmed.')
                break
            elif char_count > self.max_chars:
                print('Warning: Memory limit reached. String may be trimmed.')
                break
            else:
                output += ch
                char_count += 1

        return output

    def create_gif(self, text, filename='test.gif', imgsize=None, duration=200, loop=0):

        if not imgsize:
            imgsize = self.canvas_width, self.canvas_height
        else:
            pass

        img_seed = Image.new('RGB', imgsize, self.bg_color)
        font = ImageFont.truetype(self.font_file, self.fontsize)

        ctr = 0
        images = [img_seed]

        text = self.parse(text)

        for ind in range(len(text)):
            print('{0}/{1} frames'.format(ind + 1, len(text)))
            if text[ind] != '\n':
                frame = img_seed.copy()
                d = ImageDraw.Draw(frame)
                d.text((10, 10), text[: ind + 1], fill=self.fg_color, font=font)
                ctr = ctr + 1
                images.append(frame)
            else:
                continue

        images[0].save(filename, save_all=True, append_images=images[1:],
                       optimize=True, duration=duration, loop=loop)

