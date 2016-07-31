import configparser
from PIL import Image, ImageEnhance

config = configparser.ConfigParser()
config.read("resizer.cfg")
pathAndSize = config["RESIZER"]

imgWidth = int(pathAndSize["width"])
imgHeight = int(pathAndSize["height"])

#open and resize image
imgUnchang = Image.open(pathAndSize["pathToGet"]).convert('RGBA')
imgResiz = imgUnchang.resize((imgWidth,imgHeight))
"""open watermark image and make it's opacity reduced
split() - splitting an “RGBA” image creates three new images each containing
a copy of one of the original bands (red, green, blue,alpha)"""
watermark = Image.open(pathAndSize["pathWater"]).convert('RGBA')
alpha = watermark.split()[3]
alpha = ImageEnhance.Brightness(alpha).enhance(0.3)#reduce the brightness or the 'alpha' band
watermark.putalpha(alpha)#replaces the alpha layer in this image
watermark = watermark.resize((imgWidth,imgHeight))#resized watermark
# create a transparent layer the size of the image and draw the
# watermark in that layer.
layer = Image.new('RGBA',(imgWidth,imgHeight), (0,0,0,0))
layer.paste(watermark)
#create composite image by blending images using a transparency mask.
imgResizWithWaterm = Image.composite(layer,imgResiz,layer)

imgResizWithWaterm.save(pathAndSize["pathToSave"])

