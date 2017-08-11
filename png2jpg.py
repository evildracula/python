# from psd_tools import PSDImage
import os
from PIL import Image, ImageEnhance, ImageFilter, ImageDraw, ImageFont

for fname in os.listdir('./png'):
    fn, ext = fname.split('.')
    if ext == 'png':
        print(fname)
        im = Image.open('./png/%s' % fname)
        im.save('./png/%s.jpg' % fn, 'JPEG')
        # print('%s %s %s' % (fname, fn, ext))
        # psd = PSDImage.load('./psd/%s'% fname)
        # img = psd.as_PIL()
        # img.save('./psd/%s.png' % fn)
# for folderName, subFolders, filenames in os.walk('./psd'):
#     for filename in filenames:
#         print(filename)
