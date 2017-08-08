# -*- coding: UTF-8 -*-
import numpy as np

# arr = np.array([1,2,3,4])
# arr2 = np.array([[2,2,2],[3,3,3],[3,3,3],[3,3,3]])
# # print(arr*arr2)
# print(np.dot(arr,arr2))
# print(dir(np))

arr = np.array([1,1,1])
arr2 = np.array([3,2,1])
print(np.mean(arr))
# print(arr - arr2)
# print(arr*arr2)
# print (1 -arr2)
# print(arr2*(1-arr2)*(arr-arr2))

def nn(sample, inputsize, outputsize, hiddensize):
    # max1 = np.zeros((inputsize,hiddensize), 'd')
    # max2 = np.zeros((hiddensize,outputsize), 'd')
    max1 = np.random.uniform(-1, 1,size=[inputsize,hiddensize])
    max2 = np.random.uniform(-1, 1, size=[hiddensize, outputsize])
    print('max1 size %s max2 size %s' % (max1.shape, max2.shape))
    print('max1 %s \nmax2 %s' % (max1, max2))
    isEnd = False
    # while not isEnd:
    for s in sample:
        inputsample = s[0]
        hiddenresult = np.dot(inputsample, max1)
        result = np.dot(hiddenresult, max2)
        target = np.array(s[1])
        print('target shape %s' % target.shape)
        print('result shape %s' % result.shape)
        delta2 = result*(1-result)*(target-result)
        print('delta2: %s' % delta2)

        delta1 = max2*delta2#*hiddenresult*(1-hiddenresult)
        print('hs*(1-hs) %s' % (hiddenresult*(1-hiddenresult)))
        print('delta1: %s' % delta1)


        # s = [(x,y) for x in result for y in s[1]]
        # print(s)
        # print('result %s' % result)

sample = [
    ([1,1,1,1], [0,1]),
    ([0,1,1,1], [1,0])
]


# nn(sample, 4,2,3)