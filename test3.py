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
from PIL import Image, ImageEnhance, ImageFilter


def sendRequest2(url, headers, body):
    req = urllib.request.Request(url)
    req.set_proxy('proxy.sin.sap.corp:8080', 'http')
    for k, v in headers.items():
        req.add_header(k, v)
    response = urllib.request.urlopen(req)
    print(response.read())
    return (response.code, '', response.read())


def sendRequest(url, headers, body):
    ssl._create_default_https_context = ssl._create_unverified_context
    req = urllib.request.Request(url)
    req.set_proxy('proxy.sin.sap.corp:8080', 'http')
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


def getWXToken(appId, secret):
    url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s"
    url = url % (appId, secret)
    headers = {}
    headers['Content-Type'] = 'application/json'
    body = b""
    (code, reason, result) = sendRequest(url, headers, body)
    return json.loads(result.decode('utf-8'))


def getWXJSAPITicket(accessToken):
    url = "https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token=%s&type=jsapi"
    url = url % accessToken
    headers = {}
    headers['Content-Type'] = 'application/json'
    body = b""
    (code, reason, result) = sendRequest(url, headers, body)
    return json.loads(result.decode('utf-8'))


# access_token = getWXToken('wx9f248acc2b1a683b','e26c5dac6f18a94a11cb1bd72ec5b897')['access_token']
# print(access_token)
# jsapiticket = getWXJSAPITicket(access_token)
# print(jsapiticket)

def getSign(noncestr, ticket, timestamp, url):
    parameters = {
        'jsapi_ticket': ticket,
        'noncestr': noncestr,
        'timestamp': timestamp,
        'url': url
    }
    sortedParameters = [(k, parameters[k]) for k in sorted(parameters.keys())]
    parameterString = urllib.parse.urlencode(sortedParameters, safe=':/?=')
    print(parameterString)
    result = hashlib.sha1(parameterString.encode('utf-8'))
    print(result.hexdigest())
    return result.hexdigest()


chars = ["a", "b", "c", "d", "e", "f", "g", "h",
         "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
         "u", "v", "w", "x", "y", "z", "0", "1", "2", "3", "4", "5",
         "6", "7", "8", "9", "A", "B", "C", "D", "E", "F", "G", "H",
         "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
         "U", "V", "W", "X", "Y", "Z"
         ]
s = 'http://www.young-sun.com'


def randomChar(length):
    return ''.join([random.choice(string.ascii_letters) for x in range(length)])


def hand(seg):
    v = string.atol(seg, 16)
    v = v & 0x3FFFFFFF
    char = ''
    for i in range(6):
        idx = v & 0x0000003D
        char += chars[int(idx)]
        v = v >> 5
    return char


def sendRequest(url, headers, body):
    # ssl._create_default_https_context = ssl._create_unverified_context
    req = urllib.request.Request(url)
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


def getIpInfo(ip):
    url = "http://ip.taobao.com/service/getIpInfo.php?ip=%s" % ip
    headers = {}
    headers['Content-Type'] = 'application/json'
    print(url)
    body = b""
    (code, reason, result) = sendRequest(url, headers, body)
    return json.loads(result.decode('utf-8'))


def getIpLocation(ip):
    result = getIpInfo(ip)
    if result['code'] == 0:
        location = '%s%s%s%s%s' % (
            result['data']['country'],
            result['data']['area'],
            result['data']['region'],
            result['data']['city'],
            result['data']['isp']
        )
        return location
    else:
        return 'N/A'


# print(getIpLocation('114.61.230.73'))



def getBaiduAPIToken(apiKey, secretKey):
    url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=%(clientId)s&client_secret=%(clientSecret)s" % {
        'clientId': apiKey,
        'clientSecret': secretKey
    }
    print(url)
    headers = {}
    # headers['Content-Type'] = 'application/json'
    body = b""
    (code, reason, result) = sendRequest(url, headers, body)
    print(code)
    print(reason)
    print(result)
    return result


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


baiduApiKey = 'MtxmcKOG44KGoxngiFHneaTz'
baiduSecretKey = '9vk2KnoLOchxqVOavFsgOqtY8G2OGaGZ'

# result = getBaiduAPIToken(baiduApiKey, baiduSecretKey)
# print(result)

# b'{"access_token":"24.8263e1ea1626e1343ee995e71dad0288.2592000.1504230788.282335-9958853","session_key":"9mzdA5gmmov7X2D6FSHYCiSZvw9zVmhN7exVs+HUWrsKJnRMDl0HCuO3J2xv3bKDaRFc3jbGOppQKeyMxcd7Cd5AKxNv","scope":"public vis-faceverify_faceverify vis-faceattribute_faceattribute vis-faceverify_faceverify_v2 brain_all_scope wise_adapt lebo_resource_base lightservice_public hetu_basic lightcms_map_poi kaidian_kaidian wangrantest_test wangrantest_test1 bnstest_test1 bnstest_test2 vis-classify_flower","refresh_token":"25.1c2618eceeb270b6dd2bc940f6a86bab.315360000.1816998788.282335-9958853","session_secret":"00c3d619d02c3ba5fe822e6c1925560e","expires_in":2592000}\n'
baiduAccessToken = '24.4f4834808c48b1a20a26c3f310c484ab.2592000.1504243948.282335-9958853'
filename = 'mirei.jpg'
f = open(filename, 'rb')
im = Image.open(f)
faceIm = Image.open('face.jpg')
im.thumbnail((400, 400))
im.save('updated.jpg', 'JPEG')
f = open('updated.jpg', 'rb')
data = f.read()
base64edData = base64.b64encode(data)
urlencodedBase64edData = urllib.parse.quote(base64edData)
# for l in f:
#     # print(l)
#     data = data + l
# print(str(data,'utf-8'))
result = postAIPDectect(urlencodedBase64edData.encode(), baiduAccessToken)
# location = result['result'][0]['location']
# rotationAngle = result['result'][0]['rotation_angle']
location = {"left": 94, "top": 96, "width": 95, "height": 87}
# rotationAngle = -5

# if rotationAngle:
#     im = im.rotate(rotationAngle, expand=True)
#     size = im.size
#     location = {
#         'top': location['left'],
#         'left': size[0] - location['top'],
#         'width': location['width'],
#         'height': location['height']
#     }
box = (location['left'], location['top'], location['left'] + location['width'],
       location['top'] + location['height'])
im = im.crop(box)
im = ImageEnhance.Contrast(im).enhance(2)
im = im.convert('L')
im = im.filter(ImageFilter.CONTOUR)

p = (101, 82)
s = im.size
loc = (p[0], p[1], p[0] + s[0], p[1] + s[1])
faceIm.paste(im, loc)
# print(faceIm.size)
faceIm.show()
# im.show()
# # im.filter(ImageFilter.GaussianBlur)
# im = im.filter(ImageFilter.MedianFilter)
# r, g, b = im.split()
# r = r.point(lambda i: 1 if i > 100 else 255)
# g = g.point(lambda i: 1 if i > 100 else 255)
# b = b.point(lambda i: 1 if i > 100 else 255)
#
# def adjust(i):
#     print(i)
#     return i * 0.8 if i < 100 else i * 1.7
# # im = im.point(adjust)
# # im = Image.merge(im.mode, (r, g, b))
# # im.convert('1',colors=1)
# im.save('updated.jpg', 'JPEG')

#
# im90 = im.rotate(-90, expand=True)
#
# # newBox = (location['top'], location['left'], box[2], box[3])
#
# size = im90.size
# print(size)
#
# newLocation = {
#     'top': location['left'],
#     'left': size[0] - location['top'],
#     'width': location['width'],
#     'height': location['height']
# }
#
# # box = (newLocation['top'], newLocation['left'], newLocation['left'] + newLocation['width'], newLocation['top'] + newLocation['height'] )
# box = (newLocation['left'],newLocation['top'], newLocation['left'] + newLocation['width'], newLocation['top'] + newLocation['height'] )
#
# print(box)
# im90 = im90.crop(box)
# im90.save('updated.jpg', 'JPEG')
# # newIm = im.rotate(-90, expand=True).save('updated.jpg', 'JPEG')
# # newIm = Image.open(open('updated.jpg', 'rb'))
# # newIm.crop(box)
# # print(newIm.size)
# # newIm.save('updated.jpg', 'JPEG')
