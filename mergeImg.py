from PIL import Image, ImageEnhance, ImageFilter, ImageDraw, ImageFont
import re

def merge(file1, file2, resultfile):
    im1 = Image.open(open(file1,'rb'))
    im2 = Image.open(open(file2,'rb'))
    size1 = im1.size
    size2 = im2.size
    print('file1 size %d %d' % size1)
    print('file2 size %d %d' % size2)
    # newSize = (size1[0] + size2[0], size1[1] if size1[1] > size2[1] else size2[1])
    newSize = (size1[0] if size1[0] > size2[0] else size2[0], size1[1] + size2[1])
    print('new size %d %d' % newSize)
    newImg = Image.new('RGBA', newSize)
    newImg.paste(im1, (0,0, size1[0], size1[1]))
    newImg.paste(im2, (0,size1[1], size2[0], size1[1]+ size2[1]))
    newImg.save('%s.jpg' % resultfile,'JPEG')
    # newImg.show()

def genImageFromText(text, imageName):
    actLength = 0
    lines = []
    j = 0
    subline = []
    for i in range(len(text)):
        j = j + 1
        if re.match('[\\w\\s\\d]', text[i]):
            actLength = actLength + 1
        else:
            actLength = actLength + 2
        subline.append(text[i])
        if actLength % 14 == 0:
            lines.append(''.join(subline))
            subline = []
    if subline:
        lines.append(''.join(subline))
    height = len(lines) * 80
    im = Image.new("RGB", (360, height), (205, 255, 255))
    dr = ImageDraw.Draw(im)
    font = ImageFont.truetype("./msyh.ttc", 50)
    y = 0
    for l in lines:
        dr.text((10, 5+y), l, font=font, fill="#4e6cb4")
        y = y + 80
    im.show()
    im.save(imageName)

def drawTextOnImg(text, img, fontSize, fontColor):
    actLength = 0
    lines = []
    j = 0
    subline = []
    for i in range(len(text)):
        j = j + 1
        if re.match('[\\w\\s\\d]', text[i]):
            actLength = actLength + 1
        else:
            actLength = actLength + 2
        subline.append(text[i])
        if actLength % 20 == 0:
            lines.append(''.join(subline))
            subline = []
    if subline:
        lines.append(''.join(subline))
    height = len(lines) * 80
    # im = Image.new("RGB", (360, height), (205, 255, 255))
    dr = ImageDraw.Draw(img)
    font = ImageFont.truetype("./msyh.ttc", fontSize)
    y = 0
    for l in lines:
        # for w in l:
        # dr.text((110, 5 + y), w, font=font, fill=fontColor)
        dr.text((110, 5+y), l, font=font, fill=fontColor)
        y = y + 80
    return img


# merge('id1.jpg','id2.jpg', 'id-updated')
origin = Image.open(open('pic.jpg','rb'))
originsize = origin.size
print(originsize)
p1 = (0, 828)
p2 = (0, 900)
# box = (p[0],p[1], p[0] + s[0], p[1] + s[1])
upbox = (0, 0, originsize[0], p1[1])
upImg = origin.crop(upbox)
downbox = (0, 900, originsize[0], originsize[1])
downImg = origin.crop(downbox)
# downImg.show()
# upImg.show()

txtSize = (originsize[0], 100)
txtImg = Image.new('RGBA', txtSize,(255,255,255))
txtColor = '#333'
lnkColor = '#507daf'
txtImg = drawTextOnImg(u'这里都是动态评上去的不要问我怎么做的', txtImg, 24, lnkColor)
# txtImg.show()
resultImg = Image.new('RGBA', (originsize[0], originsize[1]+txtSize[1]))
resultImg.paste(upImg, upbox)
resultImg.paste(txtImg, (0, p1[1], txtSize[0], p1[1]+txtSize[1]))
resultImg.paste(downImg, (0, p2[1], txtSize[0], p2[1] + downImg.size[1]))
resultImg.show()