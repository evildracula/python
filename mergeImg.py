from PIL import Image, ImageEnhance, ImageFilter, ImageDraw, ImageFont
import re
import math


def merge(file1, file2, resultfile):
    im1 = Image.open(open(file1, 'rb'))
    im2 = Image.open(open(file2, 'rb'))
    size1 = im1.size
    size2 = im2.size
    print('file1 size %d %d' % size1)
    print('file2 size %d %d' % size2)
    # newSize = (size1[0] + size2[0], size1[1] if size1[1] > size2[1] else size2[1])
    newSize = (size1[0] if size1[0] > size2[0] else size2[0], size1[1] + size2[1])
    print('new size %d %d' % newSize)
    newImg = Image.new('RGBA', newSize)
    newImg.paste(im1, (0, 0, size1[0], size1[1]))
    newImg.paste(im2, (0, size1[1], size2[0], size1[1] + size2[1]))
    newImg.save('%s.jpg' % resultfile, 'JPEG')
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
        dr.text((10, 5 + y), l, font=font, fill="#4e6cb4")
        y = y + 80
    im.show()
    im.save(imageName)


# margin - (left, top, right, down)
def drawTextOnImgold(text, img, fontSize, margin=(0, 0, 0, 0), fontColor='#333', linkColor='#507daf'):
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
    print('font size %s' % (font.getsize(text),))
    y = 0
    for l in lines:
        # for w in l:
        # dr.text((110, 5 + y), w, font=font, fill=fontColor)
        dr.text((30, 5 + y), l, font=font, fill=fontColor)
        y = y + 80
    return img


# text = u"Test how long this text is 包含中文"
# txtImg = getTextImage(text, 24, 200, (10,10,10,10))
# txtImg.show()
def splitImage(img, top, bottom):
    originsize = img.size
    p1 = (0, top)
    p2 = (0, bottom)
    upbox = (0, 0, originsize[0], p1[1])
    upImg = img.crop(upbox)
    downbox = (0, bottom, originsize[0], originsize[1])
    downImg = img.crop(downbox)
    return (upbox, upImg, downbox, downImg)


# def getTextImage(text, fontSize, max_width, padding=(0, 0, 0, 0), fontColor='#333', linkColor='#507daf'):
#     font = ImageFont.truetype("msyh.ttc", fontSize)
#     textSize = font.getsize(text)
#     possibleLines = math.ceil(textSize[0] / max_width)
#     print('possibleLine %d' % possibleLines)
#     possibleContainerSize = (max_width + padding[0] + padding[2]+ int(fontSize/2), possibleLines * textSize[1] + padding[1] + padding[3])
#     txtImg = Image.new('RGBA', possibleContainerSize, (255, 255, 255))
#     dr = ImageDraw.Draw(txtImg)
#     tmpText = ''
#     charIdx = 0
#     lineIdx = 0
#     for charIdx in range(len(text)):
#         # print(text[charIdx])
#         tmpText += text[charIdx]
#         tmpTextSize = font.getsize(tmpText)
#         if tmpTextSize[0] > max_width or charIdx == len(text) - 1:
#             print('tmpTextSize width %d' % tmpTextSize[0])
#             print(tmpText)
#             dr.text((padding[0], 0 + lineIdx * textSize[1]), tmpText, font=font, fill=fontColor)
#             tmpText = ''
#             lineIdx += 1
#     return txtImg

def drawLine(dr, point, text, font):
    # dr.text(point, text, font=font, fill=color)
    p = point[0]
    link = False
    for i in text:
        w = font.getsize(i)[0]
        print(w)
        if i == '@':
            link = True
        if link and i in [',', ' ']:
            link = False
        if link:
            color = '#507daf'
        else:
            color = '#333'
        dr.text((p, point[1]), i, font=font, fill=color)
        p += w


def getTextImage(text, fontSize, max_width, padding=(0, 0, 0, 0)):
    font = ImageFont.truetype("msyh.ttc", fontSize)
    textSize = font.getsize(text)
    textLines = []
    tmpText = ''
    for charIdx in range(len(text)):
        tmpText += text[charIdx]
        tmpTextSize = font.getsize(tmpText)
        if tmpTextSize[0] > max_width:
            print(tmpText)
            textLines.append(tmpText)
            tmpText = ''
    if tmpText:
        textLines.append(tmpText)
    print(textLines)
    print('possibleLine %d' % len(textLines))
    possibleContainerSize = (
        max_width + padding[0] + padding[2] + int(fontSize / 2), len(textLines) * textSize[1] + padding[1] + padding[3])
    txtImg = Image.new('RGBA', possibleContainerSize, (255, 255, 255))
    dr = ImageDraw.Draw(txtImg)
    for line in range(len(textLines)):
        print(textLines[line])
        point = (padding[0], 0 + line * textSize[1])
        drawLine(dr, point, textLines[line], font)
    return txtImg


def addTextToImg(bgImg, top, bottom, text):
    picSize = (345, 345)
    maxTextWidth = 640
    fontSize = 24
    textPadding = (30, 10, 10, 10)
    picLeftPadding = 35
    s = bgImg.size
    upbox, upImg, downbox, downImg = splitImage(bgImg, top, bottom)
    txtImg = getTextImage(text, fontSize, maxTextWidth, textPadding)
    resultImg = Image.new('RGBA', s, (255, 255, 255))
    resultImg.paste(upImg, upbox)
    resultImg.paste(txtImg, (0, top, txtImg.size[0], top + txtImg.size[1]))
    picImg = Image.new('RGBA', picSize, (111, 111, 111))
    resultImg.paste(picImg, (
        picLeftPadding, top + txtImg.size[1] + 10, picLeftPadding + picSize[0], top + txtImg.size[1] + 10 + picSize[1]))
    resultImg.paste(downImg, (0, s[1] - downImg.size[1], downImg.size[0], s[1]))
    return resultImg


bgImg = Image.open(open(u'./psd/刘诗诗.png', 'rb'))
bgImg = addTextToImg(bgImg, 670, 1155, u'无尽的阳光 无限的蔚蓝 时光静止在Capri海岛上  心情停留在明媚风景中   这才是假期的正确打开方式  我和@abd 去看海啦')
# bgImg = addTextToImg(bgImg, 670, 490,
#                      'so')
bgImg.show()
# top = 670
# height = 50
# s = bgImg.size
# ra = (0, 670, s[0], 50)
# upbox, upImg, downbox, downImg = splitImage(bgImg, top, height)
# text = 'test test test test testest test test test test test test test'
# txtImg = getTextImage(text, 24, 640, (30,10,10,10))
# resultImg = Image.new('RGBA', (s[0], s[1]+txtImg.size[1]), (255,255,255))
# resultImg.paste(upImg, upbox)
# resultImg.paste(txtImg, (0, top, txtImg.size[0], top+txtImg.size[1]))
# resultImg.paste(downImg, (0, top+txtImg.size[1], downImg.size[0], top+txtImg.size[1] + downImg.size[1]))
# resultImg.show()




# txtSize = (originsize[0], 100)
# txtImg = Image.new('RGBA', txtSize,(255,255,255))

#
# print(ra)
#
# s = txtImg.size
# box = (replaceArea[0], replaceArea[1], replaceArea[0] + s[0], replaceArea[1] + s[1])
# bgImg.paste(txtImg, box)
# bgImg.show()






# # merge('id1.jpg','id2.jpg', 'id-updated')
# origin = Image.open(open('pic.jpg','rb'))
# originsize = origin.size
# print(originsize)
# p1 = (0, 828)
# p2 = (0, 900)
# # box = (p[0],p[1], p[0] + s[0], p[1] + s[1])
# upbox = (0, 0, originsize[0], p1[1])
# upImg = origin.crop(upbox)
# downbox = (0, 900, originsize[0], originsize[1])
# downImg = origin.crop(downbox)
# # downImg.show()
# # upImg.show()
#
# txtSize = (originsize[0], 100)
# txtImg = Image.new('RGBA', txtSize,(255,255,255))
# txtColor = '#333'
# lnkColor = '#507daf'
# txtImg = drawTextOnImg(u'这里都是动态评上去的不要问我怎么做的', txtImg, 24, lnkColor)
# # txtImg.show()
# resultImg = Image.new('RGBA', (originsize[0], originsize[1]+txtSize[1]))
# resultImg.paste(upImg, upbox)
# resultImg.paste(txtImg, (0, p1[1], txtSize[0], p1[1]+txtSize[1]))
# resultImg.paste(downImg, (0, p2[1], txtSize[0], p2[1] + downImg.size[1]))
# resultImg.show()
