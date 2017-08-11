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

    def __init__(self, inputsize, outputsize, hiddensize, step=0.1):
        self.inputsize = inputsize
        self.outputsize = outputsize
        self.hiddensize = hiddensize
        self.step = step
        self.showlog = False

    def initializeMax(self):
        self.max1 = np.array([
            [0.1, 0.1, 0.1],
            [0.1, 0.1, 0.1],
            [0.1, 0.1, 0.1],
            [0.1, 0.1, 0.1]
        ])
        self.max2 = np.array([
            [0.1],
            [0.1],
            [0.1]
        ])
        # self.max1 = np.random.uniform(0, 1, size=[self.inputsize, self.hiddensize])
        # self.max2 = np.random.uniform(0, 1, size=[self.hiddensize, self.outputsize])
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

    # def forward(self, inputsample):
    #     hiddenresult = np.dot(inputsample, self.max1)
    #     n = np.linalg.norm(hiddenresult)
    #     hiddenresult = hiddenresult/n
    #     # print('hiddenresult %s' % (hiddenresult,))
    #     result = np.dot(hiddenresult, self.max2)
    #     # print('result before %s' % (result,))
    #     m = np.linalg.norm(result)
    #     result = result / m
    #     # result = np.tanh(m)
    #     # print('result after %s' % (result,))
    #     return (hiddenresult, result)
    def forward(self, inputsample):
        if self.showlog:
            print('forward start')
            print('inputsample %s' % (inputsample,))
            print('max1 %s' % (self.max1,))
        hiddenresult = np.dot(inputsample, self.max1)
        if self.showlog:
            print('hiddenresult %s' % (hiddenresult,))
        # hiddenresult = np.tanh(hiddenresult)
        if self.showlog:
            print('tanh hiddenresult %s' % (hiddenresult,))
            print('max2 %s' % (self.max2,))
        result = np.dot(hiddenresult, self.max2)
        if self.showlog:
            print('result %s' % (result,))
        # print('result before %s' % (result,))
        # result = np.tanh(result)
        if self.showlog:
            print('tanh result %s' % (result,))
        # result = np.tanh(m)
        # print('result after %s' % (result,))
            print('forward end')
        return (hiddenresult, result)

    # def backward(self, inputsample, hiddenresult, deltaresult):
    #     deltahidden = np.array(np.dot(deltaresult, self.max2.T))
    #     # print('deltahidden %s' % (deltahidden,))
    #     # s = np.array(inputsample * self.max1.T).T * deltahidden
    #     # s = np.array(inputsample * self.max1.T).T * deltahidden
    #     s = np.array(self.max1.T).T * deltahidden
    #     # s = s / np.linalg.norm(s)
    #     # print('s %s' % (s,))
    #     s = np.array(s) + self.max1
    #     # print('old max1 %s \n new max1 %s' % (self.max1, s))
    #     self.max1 = s
    #     s = np.array(hiddenresult * self.max2.T).T * deltaresult
    #     s = np.array(s) + self.max2
    #     # print('old max2 %s \n new max2 %s' % (self.max2, s))
    #     self.max2 = s
    def backward(self, inputsample, hiddenresult, deltaresult):
        if self.showlog:
            print('backward start')
        # deltahidden = np.array(np.dot(deltaresult, self.max2.T))
        deltahidden = hiddenresult*(1-hiddenresult)*np.array(np.dot(deltaresult, self.max2.T))
        # deltainput = np.array(np.dot(deltahidden, self.max1.T))
        deltainput = np.array(inputsample)*(1-np.array(inputsample))*np.array(np.dot(deltahidden, self.max1.T))
        if self.showlog:
            print('inputsample %s' % (inputsample,))
            print('deltahidden %s' % (deltahidden,))
            print('deltainput %s' % (deltainput,))
        # s = self.max1 + self.step*(inputsample * self.max1.T).T
        # s = self.max1 + self.step *(inputsample * deltahidden.T)
        s = self.max2 + self.step*(deltahidden * self.max2.T).T * deltaresult
        if self.showlog:
            print('old max2 %s \n new max2 %s' % (self.max2, s))
        self.max2 = s
        s = self.max1 + self.step * (inputsample * self.max1.T).T * deltahidden
        if self.showlog:
            print('old max1 %s \n new max1 %s' % (self.max1, s))
        self.max1 = s
        if self.showlog:
            print('backward end')
        # s = self.max2 + deltainput * self.max2
        # self.max2 = s
        # s = self.max1 + deltahidden* self.max1
        # # print('old max2 %s \n new max2 %s' % (self.max2, s))
        # self.max1 = s
        # s = self.max1 + self.max1 * deltahidden
        # print('old max1 %s \n new max1 %s' % (self.max1, s))
        # self.max1 = s
        # # print('deltahidden %s' % (deltahidden,))
        # # s = np.array(inputsample * self.max1.T).T * deltahidden
        # # s = np.array(inputsample * self.max1.T).T * deltahidden
        # s = np.array(self.max1.T).T * deltahidden
        # # s = s / np.linalg.norm(s)
        # # print('s %s' % (s,))
        # s = np.array(s) + self.max1
        # # print('old max1 %s \n new max1 %s' % (self.max1, s))
        # self.max1 = s
        # s = np.array(hiddenresult * self.max2.T).T * deltaresult
        # s = np.array(s) + self.max2
        # # print('old max2 %s \n new max2 %s' % (self.max2, s))
        # self.max2 = s

    def train(self, sample, step=0.01, time=50, squashingFunc=np.tanh):
        # max1 = np.zeros((inputsize,hiddensize), 'd')
        # max2 = np.zeros((hiddensize,outputsize), 'd')

        isEnd = False
        lastDeltaresult = None
        # while not isEnd:
        for s in sample:
            for i in range(time):
                (hiddenresult, result) = self.forward(s[0])
                target = np.array(s[1])
                deltaresult = result * (1 - result) * (target - result)
                # deltaresult = -(target - result)
                print('deltaresult %s' % (deltaresult,))
                # print('deltaresult %s' % (deltaresult,))
                deltaresult = np.array(deltaresult)
                self.backward(s[0], hiddenresult, deltaresult)
