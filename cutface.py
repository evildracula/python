from PIL import Image, ImageEnhance, ImageFilter, ImageDraw, ImageFont
import ann
import numpy as np

fn = 'tim.jpg'
img = Image.open(open(fn, 'rb'))

margin = (54, 54)
padding = (20, 20)


def getSubPic(num):
    col = (num % 5)
    row = int(num / 5)
    r = (row, col)
    # print(r)
    return r


def getPoint(location):
    return (180 * location[0] + margin[0], 180 * location[1] + margin[1])


def getthumbnailpic(num, imgsize=(8, 8)):
    loc = getSubPic(num)
    p = getPoint(loc)
    # print(p)
    b = (p[1], p[0], p[1] + 180, p[0] + 180)
    subImg = img.crop(b)
    subImg.thumbnail(imgsize)
    subImg = subImg.convert('1')
    arr = list(subImg.getdata())
    arr = map(lambda x: 0 if x == 255 else 1, arr)
    return list(arr)


# def getblankpic(imgsize=(8, 8)):
#     img = Image.new('RGBA', imgsize, (255, 255, 255))
#     img = img.convert('1')
#     arr = list(subImg.getdata())
#     arr = map(lambda x: 0.1 if x == 255 else 0.9, arr)
#     return list(arr)


def test():
    # sample = [
    #     ([1, 1, 1, 1], [1]),
    #     # ([0.9, 0.9, 0.9, 0.9], [0.9]),
    #     # # ([0, 1, 1, 1], [0.85]),
    #     # ([0, 1, 1, 1], [0.8]),
    #     # ([0, 0, 1, 1], [0.5]),
    #     # ([0, 0, 0, 1], [0.2]),
    #     ([0, 0, 0, 0], [0])
    # ]
    sample = [([1, 1, 1, 0, 1, 1, 0, 0, 1], [1]), ([0, 0, 1, 0, 1, 0, 1, 0, 0], [0])]

    # m = ann.Machine(4,1,3)
    # m.train(sample)
    # print(m.get([0,1,1,1]))
    # print(m.get([0,1,1,1]))

    m = ann.Machine(9, 1, 6)
    m.initializeMax()
    for i in range(1, 3):
        print('start')
        m.max1 = m.initMax1
        m.max2 = m.initMax2
        m.train(sample, 5 * i)
        print(m.get([1] * 9))
        print(m.get([0, 0, 0, 1, 1, 0, 0, 0, 1]))
        print(m.get([0, 0, 0, 0, 0, 0, 0, 0, 1]))
        print('end')


def imgTest():
    imgsize = (16, 16)
    # result = [0.9, 0.1, 0.9, 0.1, 0.9, 0.1, 0.1, 0.1, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.1, 0.1, 0.9, 0.1, 0.9, 0.9,
    #           0.1, 0.1, 0.1, 0.9]
    result = [
        [0.9, 0.1],
        [0.1, 0.9],
        [0.9, 0.1],
        [0.1, 0.9],
        [0.9, 0.1],
        [0.1, 0.9],
        [0.1, 0.9],
        [0.1, 0.9],
        [0.9, 0.1],
        [0.9, 0.1],
        [0.9, 0.1],
        [0.9, 0.1],
        [0.9, 0.1],
        [0.9, 0.1],
        [0.9, 0.1],
        [0.1, 0.9],
        [0.1, 0.9],
        [0.9, 0.1],
        [0.1, 0.9],
        [0.9, 0.1],
        [0.9, 0.1],
        [0.1, 0.9],
        [0.1, 0.9],
        [0.1, 0.9],
        [0.9, 0.1]
    ]

    result = [[0.99, 0.01], [0.01, 0.99]]
    r = len(result)
    train_data = [(getthumbnailpic(x, imgsize), result[x]) for x in range(r)]
    print(train_data)
    # train_data = [
    #     (getthumbnailpic(0,imgsize), [1]),
    #     (getthumbnailpic(1,imgsize), [-1]),
    #     (getthumbnailpic(2, imgsize), [1]),
    #     (getthumbnailpic(3, imgsize), [-1]),
    #     (getthumbnailpic(4, imgsize), [-1]),
    #     (getthumbnailpic(4, imgsize), [-1]),
    #     (getthumbnailpic(4, imgsize), [-1]),
    #     (getthumbnailpic(4, imgsize), [-1]),
    #     (getthumbnailpic(4, imgsize), [-1]),
    # ]
    length = imgsize[0] * imgsize[1]
    m = ann.Machine(length, 2, 4)
    m.initializeMax()
    m.train(train_data, step=0.1, time=1)
    # print('max1 %s ' % (m.max1,))
    # print('max2 %s ' % (m.max2,))
    for i in range(10):
        s = getthumbnailpic(i, imgsize)
    # print(s)
        print('%d: %s' % (i, m.get(s),))



def chardraw(arr, size):
    s = ''
    l = len(arr)
    for i in range(1, l + 1):
        s = s + (str(arr[i - 1]) if arr[i - 1] == 1 else ' ')
        if i % size[0] == 0:
            print('%s' % s)
            s = ''


def readimgs(fn):
    img = Image.open(open(fn, 'rb'))
    img = img.convert('1')
    arr = list(img.getdata())
    arr = map(lambda x: 0 if x == 255 else 1, arr)
    return list(arr)


def imgTest2():
    imgsize = (3, 3)
    train_data = [
        (readimgs('s.jpg'), [1]),
        (readimgs('s2.jpg'), [0]),
        # (getthumbnailpic(1,imgsize), [0])
    ]
    print(train_data)
    length = imgsize[0] * imgsize[1]
    m = ann.Machine(length, 1, 2)
    m.initializeMax()
    m.train(train_data, time=5000)
    # s = getthumbnailpic(1,imgsize)
    # print(s)
    target = readimgs('s-t.jpg')
    print(target)
    print(m.get(target))


imgTest()
# test()
# print(readimgs())
# imgTest()
# test()
# chars = [1,1,1,0]
# size = (32,32)
# chardraw(getthumbnailpic(1, size), size)
# s = np.array([1,1])
# s2 = np.linalg.norm(s)
# print(s2)
