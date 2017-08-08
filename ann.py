# -*- coding: UTF-8 -*-
import numpy as np
import math

# arr = np.array([1,2,3,4])
# arr2 = np.array([[2,2,2],[3,3,3],[3,3,3],[3,3,3]])
# # print(arr*arr2)
# print(np.dot(arr,arr2))
# print(dir(np))

arr = np.array([1, 2, 3, 4])
arr2 = np.array([[2, 2, 4], [3, 3, 3], [1, 2, 3], [4, 3, 3]])


# print(arr2.T)
# print(arr*arr2.T)
# print(arr.T)
# arr2 = np.array([3,2,1])
# print(np.mean(arr))
# print(arr - arr2)
# print(arr*arr2)
# print (1 -arr2)
# print(arr2*(1-arr2)*(arr-arr2))

class Machine(object):
    max1 = None
    max2 = None

    def get(self, sample):
        hiddenresult = np.tanh(np.dot(sample, self.max1))
        result = np.dot(hiddenresult, self.max2)
        result = np.tanh(result)
        return result

    def train(self, sample, inputsize, outputsize, hiddensize, step=0.1):
        # max1 = np.zeros((inputsize,hiddensize), 'd')
        # max2 = np.zeros((hiddensize,outputsize), 'd')
        self.max1 = np.random.uniform(0, 1, size=[inputsize, hiddensize])
        self.max2 = np.random.uniform(0, 1, size=[hiddensize, outputsize])
        # print('max1 size %s max2 size %s' % (max1.shape, max2.shape))
        # print('max1 %s \nmax2 %s' % (max1, max2))
        isEnd = False
        lastDeltaresult = None
        # while not isEnd:
        for i in range(50):
            for s in sample:
                inputsample = s[0]
                hiddenresult = np.tanh(np.dot(inputsample, self.max1))
                result = np.dot(hiddenresult, self.max2)
                result = np.tanh(result)
                target = np.array(s[1])
                # print('target shape %s' % target.shape)
                # print('result shape %s' % result.shape)
                deltaresult = result * (1 - result) * (target - result)
                print('deltaresult %s' % (deltaresult,))
                deltaresult = np.array(deltaresult)
                # if lastDeltaresult:
                #     isEnd = True if deltaresult > lastDeltaresult else False
                # lastDeltaresult = deltaresult
                # print('delta2: %s' % deltaresult)
                # print('delta2 shape %s' % (deltaresult.shape))
                # print('max2 T shape %s' % (max2.T.shape,))
                deltahidden = np.array(np.dot(deltaresult, self.max2.T))
                # print(deltahidden.shape)
                s = np.array(inputsample * self.max1.T).T * deltahidden
                s = np.array(s) + self.max1
                self.max1 = s
                s = np.array(hiddenresult * self.max2.T).T * deltaresult
                s = np.array(s) + self.max2
                self.max2 = s
                # print(s)
                # print('max1 size %s max2 size %s' % (max1.shape, max2.shape))
                # print('max1 %s \nmax2 %s' % (max1, max2))
                # print(np.dot(deltahidden, max1.T))
                # max1 = max1 + step*hiddenresult*inputsample


                # delta1 = max2*delta2*hiddenresult.T*(1-hiddenresult.T)
                # print('hs*(1-hs) %s' % (hiddenresult*(1-hiddenresult)))
                # print('delta1: %s' % delta1)


                # s = [(x,y) for x in result for y in s[1]]
                # print(s)
                # print('result %s' % result)


# sample = [
#     ([1, 1, 1, 1], [1, 1]),
#     ([0, 1, 1, 1], [1, 0]),
#     ([0, 0, 1, 1], [0, 1]),
#     ([0, 0, 0, 1], [0, 0])
# ]
# m = Machine()
# m.train(sample, 4, 2, 3)
# print(m.get([0,1,1,1]))
# print(m.get([0,1,1,1]))

sample = [
    ([1, 1, 1, 1], [1]),
([0.9, 0.9, 0.9, 0.9], [1]),
    ([0, 1, 1, 1], [1]),
    ([0, 0, 1, 1], [0]),
    ([0, 0, 0, 1], [0]),
([0, 0, 0, 0], [0])
]
m = Machine()
m.train(sample, 4, 1, 2)
print(m.get([1,1,1,1]))
print(m.get([0,0,0,1]))
print(m.get([1,0,0,1]))