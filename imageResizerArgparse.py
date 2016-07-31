import argparse
from PIL import Image, ImageEnhance

parser = argparse.ArgumentParser(\
    formatter_class=argparse.RawDescriptionHelpFormatter,\
    description="""Image resizer:
    1. takes picture from the first folder
    2. Resize the picture
    3. Place a watermark
    4. Save new picture in the second folder
sample of input: d:\Folder\FirstFileName.jpg d:\Folder\SecondFileName.jpg 300-400 d:\Folder\WatermarkFileName.jpg""")

parser.add_argument('resize', type=str, nargs='+',
                    help="input format: path to folder with original image, path to\
                    folder with resized image, size of new image(heigh-width), path\
                    to folder with watermark")

args = parser.parse_args()

obj = {
    'pathToGet': args.resize[0],
    'pathToSave': args.resize[1],
    'sizeHeight': int(args.resize[2].split('-')[0]),
    'sizeWidth': int(args.resize[2].split('-')[1]),
    'pathWater': args.resize[3]
}

#open and resize image
imgUnchang = Image.open(obj['pathToGet']).convert('RGBA')
imgResiz = imgUnchang.resize((obj['sizeWidth'],obj['sizeHeight']))
"""open watermark image and make it's opacity reduced
split() - splitting an “RGBA” image creates three new images each containing
a copy of one of the original bands (red, green, blue,alpha)"""
watermark = Image.open(obj['pathWater']).convert('RGBA')
alpha = watermark.split()[3]
alpha = ImageEnhance.Brightness(alpha).enhance(0.3)#reduce the brightness or the 'alpha' band
watermark.putalpha(alpha)#replaces the alpha layer in this image
watermark = watermark.resize((obj['sizeWidth'],obj['sizeHeight']))#resized watermark
# create a transparent layer the size of the image and draw the
# watermark in that layer.
layer = Image.new('RGBA',(obj['sizeWidth'],obj['sizeHeight']), (0,0,0,0))
layer.paste(watermark)
#create composite image by blending images using a transparency mask.
imgResizWithWaterm = Image.composite(layer,imgResiz,layer)

imgResizWithWaterm.save(obj['pathToSave'],'jpeg')

