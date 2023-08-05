try: from PIL import Image, ImageFont, ImageDraw
except: print("pillow not found, use pip to install\n  pip install pillow")
from textwrap import wrap as wr
from requests import get
from io import BytesIO
import json, os
path = os.path.dirname(__file__)

class gquote:
    def __init__(self, base = None, headers = None, proxy = None, output = True, format = "png", fonts = None, shape="box"):
        self.base    = "https://zenquotes.io/api/random" if not base else base
        self.headers = headers
        self.proxy  = proxy
        self.format = format
        self.output = False
        self.shape  = shape
        self.shapes = {"box": [(1080, 1350), 20], "portrait": [(1080, 1920), 18]}
        if not self.shape in self.shapes: raise ValueError("box and portrait shapes are only available")
        if output:
            if type(output) is str:
                if "." in output: self.output = output
                else: raise ValueError("output path should include output format e.g: /home/xd/quote.png")
            else: self.output = "./quote.png"
        self.fonts = [f"{path}/fonts/Barkentina.ttf", f"{path}/fonts/Ubuntu-Italic.ttf"]
        if fonts and type(fonts) is list and len(fonts) >= 2: self.fonts = fonts

    def run(self):
        tquote = get(self.base, headers=self.headers, proxies=self.proxy)
        if tquote.status_code != 200:
            print("bad api!", tquote.status_code)
            exit(1)
        # Edit the following according to your api
        # you should give quote and author vars
        # it will do the rest!
        tquote = json.loads(tquote.text)
        quote  = tquote[0]['q']
        self.author = "~ " + tquote[0]['a'] + " ~"
        # leave these
        self.quote  = "“" + quote + "”"
        # bwidth is text width on every line
        # wquote is list of text divided on lines
        # len(wquote) gives you no. lines
        bwidth = self.shapes[self.shape][1]
        wquote = wr(self.quote, width=bwidth)
        if len(wquote) > 7:
           while len(wquote) > 7:
                 bwidth += 1
                 wquote = wr(self.quote, width=bwidth)
        # new 16:9 image
        im   = Image.new("RGB", self.shapes[self.shape][0])
        draw = ImageDraw.Draw(im)
        # load fonts
        fontsize = 100 if bwidth == 18 else 100 - bwidth
        font  = ImageFont.truetype(self.fonts[0], fontsize)
        sfont = ImageFont.truetype(self.fonts[1], 40)
        # try to center text horz/vertical
        # padding is dist. between each line
        padding = 50;
        # determine all lines height
        w, h = draw.textsize('TEST', font=font)
        totalH = (h*len(wquote))+(padding*len(wquote))+120
        ch = (self.shapes[self.shape][0][1] - totalH) / 2
        for i in wquote:
            w, h = draw.textsize(i, font=font)
            draw.text( ( (1080-w)/2, ch), i, font=font)
            ch += h + padding
        # finally draw author with diffrent font
        w, h = draw.textsize(self.author, font=sfont)
        draw.text( ( (1080-w)/2, ch+80), self.author, font=sfont)
        # export
        if self.output: im.save(self.output)
        else: # export to memory
            out = BytesIO()
            im.save(out, format=self.format, quality=100)
            return out

        print('saved to ', self.output)
        return self.output
