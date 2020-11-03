from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


# 根据文本创建gif
class GIFGenerator:
    def __init__(self):
        pass

    def create_gif(self, text, filename='test.gif', imgsize=(600, 200), bgcolor=(255, 255, 255),
               fgcolor=(102, 8, 116), fontfile='resources/fonts/STXINGKA.ttf', fontsize=60, duration=200, loop=0):
        img_seed = Image.new('RGB', imgsize, bgcolor)
        font = ImageFont.truetype('simhei', fontsize)

        ctr = 0
        images = [img_seed]

        for i in range(len(text)):
            images.append(img_seed.copy())

        for frame in images:
            d = ImageDraw.Draw(frame)
            d.text((10, 10), text[:ctr], fill=fgcolor, font=font)
            ctr = ctr + 1

        images[0].save(filename,
                save_all=True, append_images=images[1:], optimize=False, duration=duration, loop=loop)

