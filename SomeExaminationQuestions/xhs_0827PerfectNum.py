#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project     ：MachineLearning 
@File        ：xhs_PerfectNum.py
@Description ：
题目描述：
用户的每一次点赞都代表着对内容的喜爱。小红定义一个正整数×为完美数字 当且仅当同时满足以下两个条件：
可以将 x 写作一个公差为 1 且所有元素都是正整数的等差数列的乘积，例如，6 可以写作1*2*3;
上述等差数列的长度至少为 3。
现在小红薯接收到多次 Plog 点赞数查询，每次给出一个正整数 ×,请帮助小红薯判断该点赞数是否为完美数字。
---------------
输入描述
每个测试文件均包含多组测试数据。第一行输入一个整数T
(1<T<104) 代表数据组数，每组测试数据描述如下:在一行上输入一个整数x (1<x<109) ,表示一次点赞数查询。
输出描述
对于每组测试数据，新起一行,如果点赞数是完美数字，输出YES；否则，输出 NO。
input:
3
6
2
24
output:
YES
NO
YES
@Author      ：Hello World
@Date        ：2025/8/27 下午7:34 
'''


def solve1(x) -> bool:
    # 超时？
    # 答案错误，这个是从1开始的连续等差数列，但其实从2开始从3开始也可以
    if x < 6:
        return False
    num = 1
    mul = 1
    while num < x:
        num *= mul
        mul += 1
    if num == x:
        return True
    else:
        return False


from math import sqrt

# 5
# 6
# 336
# 24
# 25
# 12
import math


def solve(x) -> bool:
    # 遍历可能的起始数字i，但限制范围
    # 起始数字i的最大值：因为至少3个数相乘，所以i最大不超过x的立方根
    max_i = (int(x ** (1 / 3)) + 2)

    for i in range(1, max_i + 1):
        num = i
        mul = i + 1
        cnt = 1
        while num < x and cnt < 20:  # 添加cnt上限防止无限循环
            num *= mul
            cnt += 1
            if num == x and cnt >= 3:
                return True
            if num > x:
                break
            mul += 1

    return False


def submit():
    import sys
    data = sys.stdin.read().split()
    t = int(data[0])
    index = 1
    results = []
    for i in range(t):
        x = int(data[index])
        index += 1
        if solve(x):
            results.append("YES")
        else:
            results.append("NO")

    for res in results:
        print(res)


submit()
