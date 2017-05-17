# -*- coding: utf-8 -*-
__author__ = 'xuxiaoye'

from math import sqrt

critics = {
    'Lisa Rose': {
        'Lady in the water': 2.5,
        'Snakes on a Plane': 3.5,
        'Just My Luck': 3.0,
        'Superman Returns': 3.5,
        'You, Me and Dupree': 2.5,
        'The Night Listener': 3.0
    },
    'Gene Seymour': {
        'Lady in the water': 3.0,
        'Snakes on a Plane': 3.5,
        'Just My Luck': 1.5,
        'Superman Returns': 5.0,
        'You, Me and Dupree': 3.0,
        'The Night Listener': 3.5
    },
    'Michael Phillips': {
        'Lady in the water': 2.5,
        'Snakes on a Plane': 3.0,
        'Superman Returns': 3.5,
        'The Night Listener': 4.0
    },
    'Claudia Puig': {
        'Snakes on a Plane': 3.5,
        'Just My Luck': 3.0,
        'Superman Returns': 4.0,
        'You, Me and Dupree': 2.5,
        'The Night Listener': 4.5
    },
    'Mick LaSalle': {
        'Lady in the water': 3.0,
        'Snakes on a Plane': 4.0,
        'Just My Luck': 2.0
    },
    'Jack Matthews': {
        'Lady in the water': 3.0,
        'Snakes on a Plane': 4.0,
        'Superman Returns': 5.0,
        'You, Me and Dupree': 3.5,
        'The Night Listener': 3.0
    },
    'Toby': {
        'Snakes on a Plane': 4.5,
        'You, Me and Dupree': 1.0,
        'Superman Returns': 4.0,
    }
}




def sim_distance(prefs, person1, person2):
    si = {}
    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item] = 1

    if len(si) == 0:
        return 0

    sum_of_squares = sum(
        [pow(prefs[person1][item] - prefs[person2][item], 2) for item in prefs[person1] if item in prefs[person2]])

    return 1 / (1 + sqrt(sum_of_squares))


def sim_pearson(prefs, person1, person2):
    si = {}
    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item] = 1

    n = len(si)
    if n == 0:
        return 1

    sum1 = sum([prefs[person1][it] for it in si])
    sum2 = sum([prefs[person2][it] for it in si])

    sum1Sq = sum([pow(prefs[person1][it], 2) for it in si])
    sum2Sq = sum([pow(prefs[person2][it], 2) for it in si])

    pSum = sum([prefs[person1][it] * prefs[person2][it] for it in si])

    num = pSum - (sum1 * sum2 / n)
    den = sqrt((sum1Sq - pow(sum1, 2) / n) * (sum2Sq - pow(sum2, 2) / n))
    if den == 0:
        return 0
    return num / den


# print sim_distance(critics, 'Lisa Rose', 'Gene Seymour')
# print sim_distance(critics, 'Lisa Rose', 'Gene Seymour')

def jaccard(p, q):
    x = set(p)
    y = set(q)
    xy = x & y
    x_y = x | y
    return float(len(xy)) / (len(x_y))


def sim_tonimoto(user_data, user1, user2):
    common = [item for item in user_data[user1] if item in user_data[user2]]
    return float(len(common)) / (len(user_data[user1]) + len(user_data[user2]) - len(common))


print sim_tonimoto(critics, 'Lisa Rose', 'Gene Seymour')


def sim_manhattan(prefs, p1, p2):
    si = {}
    for item in p1:
        if item in p2: si[item] = 1
    if len(item) == 0: return 1

    sum_of_minus = sum([abs(prefs[p1][item] - prefs[p2][item])
                        for item in prefs[p1] if item in prefs[p2]])
    return 1 / (sum_of_minus + 1)

# print u"曼哈顿距离（最后得到的数值也是相似度）："
# print sim_manhattan(critics, 'Lisa Rose', 'Gene Seymour')


def topMatchers(prefs, person, n=5, similarity=sim_pearson):
    scores=[(similarity(prefs, person, other), other) for other in prefs if other!=person]
    scores.sort()
    scores.reverse()
    return scores[:n]

print topMatchers(critics, 'Toby')

def mul(matrix_a, matrix_b):
    # 1 2   2 4    8, 16
    #       3 6
    #
    # 1 2  4 5    12 11
    # 3 1  4 3    16 18
    # n*m * m*k =  n*k
    # 1*2 * 2*3 = 1*3
    # 1 2   2 4 4  =   8, 16, 6
    #       3 6 1
    #
    # a[n][m]  b[m][k]   r[n][k] = a[n][m]*




    result = [[0]*len(matrix_a[0])]*len(matrix_b)

    # for i in range(len(result[0])):
    #     for j in range(len(result)):
    #         result[i][j] =

import numpy as np
import math
a = np.matrix([[1,2,3,4]])
b = np.matrix([[1,1],[2,2],[3,3],[4,4]])
c = np.math.tanh(a * b)
print c


