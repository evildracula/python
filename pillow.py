# -*- coding: UTF-8 -*-
import re
import hashlib
import random
import string
import urllib.request
import urllib.parse
import json
import hashlib
import ssl
import base64
from io import StringIO, BytesIO
import math

from PIL import Image, ImageEnhance, ImageFilter, ImageFont, ImageDraw


def roll(image, delta):
    "Roll an image sideways"

    image = image.copy()  # 复制图像
    xsize, ysize = image.size

    delta = delta % xsize
    if delta == 0: return image

    part1 = image.crop((0, 0, delta, ysize))
    part2 = image.crop((delta, 0, xsize, ysize))
    image.paste(part2, (0, 0, xsize - delta, ysize))
    image.paste(part1, (xsize - delta, 0, xsize, ysize))

    return image


def compress_image(img, w=128, h=128):
    '''''
    缩略图
    '''
    img.thumbnail((w, h))
    img.save('test1.png', 'PNG')
    return img


def cut_image(img):
    '''''
    截图, 旋转，再粘贴
    '''
    # eft, upper, right, lower
    # x y z w  x,y 是起点， z,w是偏移值
    width, height = img.size
    box = (width - 200, height - 100, width, height)
    region = img.crop(box)
    # 旋转角度
    region = region.transpose(Image.ROTATE_180)
    img.paste(region, box)
    img.save('test2.jpg', 'JPEG')
    return img


def logo_watermark(img, logo_path):
    '''''
    添加一个图片水印,原理就是合并图层，用png比较好
    '''
    baseim = img
    logoim = Image.open(logo_path)
    bw, bh = baseim.size
    lw, lh = logoim.size
    baseim.paste(logoim, (bw - lw, bh - lh))
    baseim.save('test3.jpg', 'JPEG')
    return baseim


def text_watermark(img, text, out_file="test4.jpg", angle=23, opacity=0.50):
    '''''
    添加一个文字水印，做成透明水印的模样，应该是png图层合并
    http://www.pythoncentral.io/watermark-images-python-2x/
    这里会产生著名的 ImportError("The _imagingft C module is not installed") 错误
    Pillow通过安装来解决 pip install Pillow
    '''
    watermark = Image.new('RGBA', img.size, (255, 255, 255))  # 我这里有一层白色的膜，去掉(255,255,255) 这个参数就好了

    FONT = "msyh.ttc"
    size = 2

    n_font = ImageFont.truetype(FONT, size)  # 得到字体
    n_width, n_height = n_font.getsize(text)
    text_box = min(watermark.size[0], watermark.size[1])
    while (n_width + n_height < text_box):
        size += 2
        n_font = ImageFont.truetype(FONT, size=size)
        n_width, n_height = n_font.getsize(text)  # 文字逐渐放大，但是要小于图片的宽高最小值

    text_width = (watermark.size[0] - n_width) / 2
    text_height = (watermark.size[1] - n_height) / 2
    # watermark = watermark.resize((text_width,text_height), Image.ANTIALIAS)
    draw = ImageDraw.Draw(watermark, 'RGBA')  # 在水印层加画笔
    draw.text((text_width, text_height),
              text, font=n_font, fill="#21ACDA")
    watermark = watermark.rotate(angle, Image.BICUBIC)
    alpha = watermark.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    watermark.putalpha(alpha)
    Image.composite(watermark, img, watermark).save(out_file, 'JPEG')


# 等比例压缩图片
def resizeImg(im, dst_w=0, dst_h=0, qua=85):
    '''''
    只给了宽或者高，或者两个都给了，然后取比例合适的
    如果图片比给要压缩的尺寸都要小，就不压缩了
    '''
    ori_w, ori_h = im.size
    widthRatio = heightRatio = None
    ratio = 1

    if (ori_w and ori_w > dst_w) or (ori_h and ori_h > dst_h):
        if dst_w and ori_w > dst_w:
            widthRatio = float(dst_w) / ori_w  # 正确获取小数的方式
        if dst_h and ori_h > dst_h:
            heightRatio = float(dst_h) / ori_h

        if widthRatio and heightRatio:
            if widthRatio < heightRatio:
                ratio = widthRatio
            else:
                ratio = heightRatio

        if widthRatio and not heightRatio:
            ratio = widthRatio

        if heightRatio and not widthRatio:
            ratio = heightRatio

        newWidth = int(ori_w * ratio)
        newHeight = int(ori_h * ratio)
    else:
        newWidth = ori_w
        newHeight = ori_h

    im.resize((newWidth, newHeight), Image.ANTIALIAS).save("test5.jpg", "JPEG", quality=qua)
    return im


# 裁剪压缩图片
def clipResizeImg(im, dst_w, dst_h, qua=95):
    '''''
        先按照一个比例对图片剪裁，然后在压缩到指定尺寸
        一个图片 16:5 ，压缩为 2:1 并且宽为200，就要先把图片裁剪成 10:5,然后在等比压缩
    '''
    ori_w, ori_h = im.size

    dst_scale = float(dst_w) / dst_h  # 目标高宽比
    ori_scale = float(ori_w) / ori_h  # 原高宽比

    if ori_scale <= dst_scale:
        # 过高
        width = ori_w
        height = int(width / dst_scale)

        x = 0
        y = (ori_h - height) / 2

    else:
        # 过宽
        height = ori_h
        width = int(height * dst_scale)

        x = (ori_w - width) / 2
        y = 0

        # 裁剪
    box = (x, y, width + x, height + y)
    # 这里的参数可以这么认为：从某图的(x,y)坐标开始截，截到(width+x,height+y)坐标
    # 所包围的图像，crop方法与php中的imagecopy方法大为不一样
    newIm = im.crop(box)
    im = None

    # 压缩
    ratio = float(dst_w) / width
    newWidth = int(width * ratio)
    newHeight = int(height * ratio)
    newIm.resize((newWidth, newHeight), Image.ANTIALIAS).save("test6.jpg", "JPEG", quality=95)
    return newIm


def getImgByFile(filename):
    return Image.open(open(filename, 'rb'))


def getImgBytesIO(filename):
    return BytesIO(open(filename, 'rb').read())


def sendRequest(url, headers, body):
    ssl._create_default_https_context = ssl._create_unverified_context
    req = urllib.request.Request(url)
    # req.set_proxy('proxy.sin.sap.corp:8080', 'http')
    for k, v in headers.items():
        req.add_header(k, v)
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor)
    try:
        response = opener.open(req, body)
        return (response.code, '', response.read())
    except urllib.request.HTTPError as e:
        return (e.code, e.reason, e.read())
    except urllib.request.URLError as e:
        return (None, e.reason, None)


def postAIPDectect(imgData, accessToken):
    url = "https://aip.baidubce.com/rest/2.0/face/v1/detect?access_token=%(accessToken)s" % {
        'accessToken': accessToken
    }
    print(url)
    headers = {}
    headers['Content-Type'] = 'application/x-www-form-urlencoded'
    body = b"image=%s" % imgData
    print(body)
    (code, reason, result) = sendRequest(url, headers, body)
    print(code)
    print(reason)
    print(result)
    if code == 200:
        return json.loads(result.decode('utf-8'))
    return {}


def resizeImg(im, dst_w=0, dst_h=0, qua=85):
    '''''
    只给了宽或者高，或者两个都给了，然后取比例合适的
    如果图片比给要压缩的尺寸都要小，就不压缩了
    '''
    ori_w, ori_h = im.size
    widthRatio = heightRatio = None
    ratio = 1

    if (ori_w and ori_w > dst_w) or (ori_h and ori_h > dst_h):
        if dst_w and ori_w > dst_w:
            widthRatio = float(dst_w) / ori_w  # 正确获取小数的方式
        if dst_h and ori_h > dst_h:
            heightRatio = float(dst_h) / ori_h

        if widthRatio and heightRatio:
            if widthRatio < heightRatio:
                ratio = widthRatio
            else:
                ratio = heightRatio

        if widthRatio and not heightRatio:
            ratio = widthRatio

        if heightRatio and not widthRatio:
            ratio = heightRatio

        newWidth = int(ori_w * ratio)
        newHeight = int(ori_h * ratio)
    else:
        newWidth = ori_w
        newHeight = ori_h

    im.resize((newWidth, newHeight), Image.ANTIALIAS).save("test5.jpg", "JPEG", quality=qua)
    return im


def detectFace(imgFile):
    f = open(imgFile, 'rb')
    targetBinData = f.read()
    base64edData = base64.b64encode(targetBinData)
    urlencodedBase64edData = urllib.parse.quote(base64edData)
    result = postAIPDectect(urlencodedBase64edData.encode(), baiduAccessToken)
    print('detect face result :%s' % result)
    return result


def changeFace(inputfile, backgroundfile, point, size):
    # Get face
    f = open(inputfile, 'rb')
    targetBinData = f.read()
    base64edData = base64.b64encode(targetBinData)
    urlencodedBase64edData = urllib.parse.quote(base64edData)
    result = postAIPDectect(urlencodedBase64edData.encode(), baiduAccessToken)
    location = result['result'][0]['location']
    rotationAngle = result['result'][0]['rotation_angle']
    print('%s %s' % (location, rotationAngle))
    targetImg = Image.open(f)
    targetImg = targetImg.rotate(rotationAngle, expand=False)
    targetImg.save('1-rotated.jpg', 'JPEG')
    targetBinData = BytesIO()
    targetImg.save(targetBinData, 'JPEG')
    base64edData = base64.b64encode(targetBinData.getvalue())
    urlencodedBase64edData = urllib.parse.quote(base64edData)
    result = postAIPDectect(urlencodedBase64edData.encode(), baiduAccessToken)
    location = result['result'][0]['location']
    rotationAngle = result['result'][0]['rotation_angle']
    targetImg = Image.open(targetBinData)
    box = (location['left'], location['top'], location['left'] + location['width'],
           location['top'] + location['height'])
    faceImg = targetImg.crop(box)
    faceImg.save('2-face.jpg', 'JPEG')
    # faceImg = resizeImg(faceImg,dst_w=s[0])
    # s = faceImg.size
    faceImg = faceImg.resize(s)
    targetImg.save('3-resizedface.jpg', 'JPEG')
    # faceImg.show()
    bgImg = Image.open(open(backgroundfile, 'rb'))
    bgImg = bgImg.convert('RGBA')
    bgImg2 = Image.new('RGBA', bgImg.size, (221, 165, 120))
    loc = (point[0], point[1], point[0] + size[0], point[1] + size[1])
    bgImg2.paste(faceImg, loc)
    bgImg2.save('4-bgface.jpg', 'JPEG')
    resultImg = Image.composite(bgImg, bgImg2, bgImg)
    resultImg.save('5-result.jpg', 'JPEG')


baiduAccessToken = '24.4f4834808c48b1a20a26c3f310c484ab.2592000.1504243948.282335-9958853'


inputfile = 'man5.jpg'
backgroundfile = 'bg2.png'
p = (116, 152)
s = (176, 169)
changeFace(inputfile, backgroundfile, p, s)
# detectFace('girl4.jpg')

# girl4.jpg {'location': {'left': 541, 'top': 282, 'width': 289, 'height': 259} 'rotation_angle': 39

# f = open(inputfile, 'rb')
# img = Image.open(f)
# img.thumbnail((200,200))
# imgBin = BytesIO()
# img.save(imgBin, 'JPEG')
# # print(imgBin)
# img2 = Image.open(imgBin)
# img2.show()
# print(imgBin.getvalue())

def getangle(degree):
    result = math.pi * degree / 180
    return result

#
# f = open('man5.jpg', 'rb')
# targetBinData = f.read()
# base64edData = base64.b64encode(targetBinData)
# urlencodedBase64edData = urllib.parse.quote(base64edData)
# result = postAIPDectect(urlencodedBase64edData.encode(), baiduAccessToken)
# location = result['result'][0]['location']
# rotationAngle = result['result'][0]['rotation_angle']
# # location = {"left":876,"top":1261,"width":641,"height":711}
# # rotationAngle = -88
# x, y, w, h = location['left'], location['top'], location['width'], location['height']
# print('%d %d %d %d' % (x, y, w, h))
# if rotationAngle < 0:
#     newX = math.fabs(math.sin(getangle(rotationAngle))) * h
#     newW = h / math.fabs(math.cos(getangle(90 - rotationAngle)))
#     newH = h - math.sin(getangle(90 - rotationAngle)) * h * 2
#     newY = y - newH
# else:
#     newX = x - math.sin(getangle(rotationAngle)) * h
#     newY = y
#     newW = h / math.cos(getangle(90 - rotationAngle))
#     newH = math.sin(getangle(90-rotationAngle)) * h * 2
# print('box %d %d %d %d' % (newX, newY, newW, newH))
# box = (newX, newY, newX+newW, newY+newH)
# print('cutbox %d %d %d %d' % box)
# originImg = Image.open(f)
# print('size %d %d' % originImg.size)
# # originImg.show()
# # originImg.crop((454,282, 454+100, 282+100)).show()
# cuttedImg = originImg.crop(box)
# cuttedImg.save('me2-cutted.jpg','JPEG')
# rotatedImg = cuttedImg.rotate(rotationAngle)
# rotatedImg.save('me2-rotated.jpg','JPEG')
#
# yy = math.sin(getangle(90-rotationAngle)) * math.sin(getangle(90-rotationAngle)) * h
# xx = math.sin(getangle(90-rotationAngle)) * (h / math.cos(getangle(90 - rotationAngle)) / 2)
# print('%d %d' % (xx, yy))