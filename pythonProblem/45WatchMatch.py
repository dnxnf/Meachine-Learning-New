#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project  ：MachineLearning 
@File     ：45WatchMatch.py
@Describe ：PyCharm 
@Author   ：Hello World
@Date     ：2025/5/28 下午12:08
为了庆祝某个重要节日（如中国共产党成立100周年），某公园将举行多场文艺表演。很多演出都是同时进行的，
一个人只能同时观看一场演出，且不能迟到早退。由于演出分布在不同的演出场地，所以连续观看的演出之间最少有15分钟的时间间隔。
小明是一个狂热的文艺迷，想观看尽可能多的演出。现在给出演出时间表，请计算小明最多能观看几场演出。
二、输入与输出
输入描述：
第一行为一个整数N，表示演出场数，1<=N<=1000。
接下来N行，每行两个空格分割的整数，第一个整数T表示演出的开始时间，第二个整数L表示演出的持续时间。
T和L的单位为分钟，0<=T<=1440，0<L<=100。
输出描述：
输出一个整数，表示小明最多能观看的演出场数。
eg:
4
10 30
20 40
40 20
60 50
out:2
'''
n = int(input())
matrix = [list(map(int, input().split())) for i in range(n)]
for x in matrix:
    x[1] += x[0]  # 把结束时间算出来。
print(matrix)


def result():
    # matrix表示开始时间，结束时间。
    matrix.sort(key=lambda x: (-x[1], -x[0]))
    s1 = matrix[0][0]  # 最大的开始时间，
    ans = 1
    for s2, e2 in matrix:
        if s1 - e2 > 15:
            ans += 1
            s1 = s2  # 更新s1的值，用来比较下一个。
    return ans


print(result())
