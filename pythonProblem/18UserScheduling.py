#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project  ：MachineLearning 
@File     ：18UserScheduling.py
@Describe ：PyCharm 
@Author   ：Hello World
@Date     ：2025/5/28 上午9:39
题目描述
在通信系统中，一个常见的问题是对用户进行不同策略的调度，会得到不同的系统消耗和性能.
假设当前有n个待串行调度用户，每个用户可以使用A/B/C三种不同的调度策略，不同的策略会消耗不同的系统资源。
请你根据如下规则进行用户调度，并返回总的消耗资源数
规则:
相邻的用户不能使用相同的调度策略，例如，第1个用户使用了A策略，则第2个用户只能使用B或者C策好
2.对单个用户而言，不同的调度策略对系统资源的消耗可以归一化后抽象为数值。
例如，某用户分别使用A/B/C策略的系统消耗分别为15/8/17。
3.每个用户依次选择当前所能选择的对系统资源消耗最少的策略(局部最优)，如果有多个满足要求的策略，选最后一个。
输入描述
第一行表示用户个数n
接下来每一行表示一个用户分别使用三个策略的系统消耗resAresBresC
输出描述
最优策略组合下的总的系统资源消耗数
用例:
3
15 8 17
12 20 9
11 7 5
out:24 (8+9+7)
'''
n = int(input())
res = [list(map(int,input().split())) for i in range(n)]
print(n)
# 3
# 15 8 7
# 12 20 9
# 11 7 5
print(res)
# 按照题目说的局部最优
import sys
def minIdx(arr, preidx):
    # 先把值搞到最大。
    minVal = sys.maxsize
    minCur = -1
    # 逐个遍历，与上一个idx要进行比对，如果相等就跳过。
    for i in range(len(arr)):
        if i == preidx:
            continue
        # 不等就比较大小，求得最小值。
        if arr[i]<=minVal:
            minVal = arr[i]
            minCur = i
    return minCur


def result():
    last = -1
    total = 0
    for i in range(n):
        # 本次不能选上次选的，然后排序，选最小的。
        last = minIdx(res[i], last)
        total += res[i][last]
    return total
print(result())
