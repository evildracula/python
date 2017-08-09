# -*- coding: UTF-8 -*-
import numpy as np
import math

class Machine(object):
    initMax1 = None
    initMax2 = None
    max1 = None
    max2 = None
    inputsize = None
    outputsize = None
    hiddensize = None

    def __init__(self, inputsize, outputsize, hiddensize):
        self.inputsize = inputsize
        self.outputsize = outputsize
        self.hiddensize = hiddensize

    def initializeMax(self):
        self.max1 = np.random.uniform(0, 1, size=[self.inputsize, self.hiddensize])
        self.max2 = np.random.uniform(0, 1, size=[self.hiddensize, self.outputsize])
        self.initMax1 = self.max1.copy()
        self.initMax2 = self.max2.copy()
        # print('max1 size %s max2 size %s' % (self.max1.shape, self.max2.shape))
        # print('max1 %s \nmax2 %s' % (self.max1, self.max2))

    def get(self, sample):
        (hiddenresult, result) = self.forward(sample)
        # hiddenresult = np.dot(sample, self.max1)
        # result = np.dot(hiddenresult, self.max2)
        # result = np.tanh(result)
        return result

    def forward(self, inputsample):
        hiddenresult = np.dot(inputsample, self.max1)
        n = np.linalg.norm(hiddenresult)
        hiddenresult = hiddenresult/n
        # print('hiddenresult %s' % (hiddenresult,))
        result = np.dot(hiddenresult, self.max2)
        # print('result before %s' % (result,))
        m = np.linalg.norm(result)
        result = result / m
        # result = np.tanh(m)
        # print('result after %s' % (result,))
        return (hiddenresult, result)

    def backward(self, inputsample, hiddenresult, deltaresult):
        deltahidden = np.array(np.dot(deltaresult, self.max2.T))
        # print('deltahidden %s' % (deltahidden,))
        # s = np.array(inputsample * self.max1.T).T * deltahidden
        # s = np.array(inputsample * self.max1.T).T * deltahidden
        s = np.array(self.max1.T).T * deltahidden
        # s = s / np.linalg.norm(s)
        # print('s %s' % (s,))
        s = np.array(s) + self.max1
        # print('old max1 %s \n new max1 %s' % (self.max1, s))
        self.max1 = s
        s = np.array(hiddenresult * self.max2.T).T * deltaresult
        s = np.array(s) + self.max2
        # print('old max2 %s \n new max2 %s' % (self.max2, s))
        self.max2 = s

    def train(self, sample, step=0.01, time=50, squashingFunc=np.tanh):
        # max1 = np.zeros((inputsize,hiddensize), 'd')
        # max2 = np.zeros((hiddensize,outputsize), 'd')

        isEnd = False
        lastDeltaresult = None
        # while not isEnd:
        for i in range(time):
            for s in sample:
                (hiddenresult, result) = self.forward(s[0])
                target = np.array(s[1])
                deltaresult = result * (1 - result) * (target - result)
                # print('deltaresult %s' % (deltaresult,))
                deltaresult = np.array(deltaresult)
                self.backward(s[0], hiddenresult, deltaresult)
