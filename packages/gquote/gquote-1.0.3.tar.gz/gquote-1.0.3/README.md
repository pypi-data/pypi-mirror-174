# Gquote

Using zen.io api this libary is able to generate Quote images  
using pillow, Detects quote length and adjust text size accordingly.  

<img src="https://raw.githubusercontent.com/Justxd22/Quote-to-PNG_XD/main/todayquote.png" width="360" height="640" alt="example"/>

## Install

Use pip to install `pip install gquote`  

Depends on:  
 - pillow
 - textwrap
 - requests

Install using pip: `pip install pillow textwrap requests`  

## Usage

This libary was designed to be as customizable as possible  

### Use proxy 

pass requests proxy format `"protocol" : "address"`  
```py
from gquote import gquote

image = gquote(proxy={"https":"127.0.0.1:8080"}).run()
```

### Change image shape/size

You can choose between two shapes portrait, or box size  
```py
from gquote import gquote

image = gquote(shape="box").run() # outputs 1080x1350
```
Or  
```py
from gquote import gquote

image = gquote(shape="portrait").run() # outputs 1080x1920
```

### Change output path or format

Pass output format as name + .png, .jpg, .jpeg  
Check <a href="https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html">pillow supported image formats for more</a>  
```py
from gquote import gquote

image = gquote(output="/home/xd/cloud/quote.jpg").run()
```

### Export to Memory

For faster output or Saving disk IO usage,  
you can save to Memory as BytesIO object  
Optionally you can choose output format  
by passing format var, default format is PNG,  
Later you can save image to disk by `getbuffer()`,  
Make sure you use same format of the output  
```py
from gquote import gquote

image = gquote(output=False, format="jpg").run()

with open('quote.jpg', 'wb') as f: # .jpg same format
    f.write(image.getbuffer())
    f.close()
```

### Use diffrent API

You can change the api to your choice,  
also you can pass headers if api requires Auth.  
```py
from gquote import gquote

image = gquote(base="https://yourapiofchoice.io/api/quote", headers={'Content-Type': 'application/json', 'Accept': '*/*', 'Origin': 'https://zenquotes.io', 'User-Agent':....}).run()
```

### Custom Fonts

You can pass fonts path of your choice,  
ttf and otf formats are supported,  
Check <a href="https://pillow.readthedocs.io/en/stable/reference/ImageFont.html">pillow docs for more supported formats,</a>  
You have to pass list of two fonts to be used,  
one for the quote, other for the author text.  
```py
from gquote import gquote

image = gquote(fonts=["/home/xd/ubutu-font.ttf", "/home/xd/ubutu-font-italic.ttf"]).run()
```

## Credits

Big thanks to zenquotes.io for their amazing freeware api  

## Donation

You can support my work by donating to the following address,  
  - XMR - `433CbZXrdTBQzESkZReqQp1TKmj7MfUBXbc8FkG1jpVTBFxY9MCk1RXPWSG6CnCbqW7eiMTEGFgbHXj3rx3PxZadPgFD3DX`
THANKS KIND SOUL!  


Find me: <a href="https://xd22.me">xd22.me</a>
