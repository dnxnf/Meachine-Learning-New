#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project  ：MachineLearning 
@File     ：44NumsSequence.py
@Describe ：PyCharm 
@Author   ：Hello World
@Date     ：2025/5/28 下午12:06
对于一个连续正整数组成的序列，可以将其拼接成一个字符串，再将字符串里的部分字符打乱顺序。
如序列8 9 10 11 12,拼接成的字符串为89101112,打乱一部分字符后得到90811211,原来的正整数10就被拆成了0和1。
现给定一个按如上规则得到的打乱字符的字符串，请将其还原成连续正整数序列，并输出序列中最小的数字。
输入描述
输入一行，为打乱字符的字符串和正整数序列的长度，两者间用空格分隔，字符串长度不超过200,正整数不超过1000,保证输入可以还
原成唯一序列。
输出描述
输出一个数字，为序列中最小的数字。
用例:
19801211 5
out:8
'''
s, k = input().split()
# 19801211 5
k = int(k)
print(s)
print(k)
def cmp(base, count):
    # 用来比较count与base差异。
    for c in base:
        # key为各个数字，value是出现的次数。
        if count.get(c) is None or count[c] != base[c]:
            return False
    return True

def countNumber(num, count, isAdd):
    for c in num: # 加，减合并成一个函数。
        count[c] = count.get(c, 0)+(1 if isAdd else -1)

def result():
    base = {}
    # 题目提供的基准。
    for c in s:
        base[c] = base.get(c,0)+1 # 这个写法我觉得很牛逼。
    # 初始化滑窗(长度为k)中各字符的数量
    count = {}
    # 题目说了连续的正整数，所以从1到k
    for i in range(1, k+1):
        countNumber(str(i), count, True)
    # 如果滑窗各字符数量和base统计的字符数量是否一致，如果一致，就说明初始化滑窗是一个符合要求的连续整数数列。
    # 该数列的最小值为1
    if cmp(base, count):
        return 1
    # 初始化滑窗没有返回，那就增加一个。滑窗长度是k。
    for i in range(2, 1000-k+2): # 开始为2，结束为1000-k+1 然后range左闭右开，需要再加1.
        # 相校于上一个滑窗新增的数字。
        remove = str(i-1)
        countNumber(remove, count, False) # 调用减去。优秀！
        # 相较于上一个滑窗增加的数字
        add = str(i+k-1)
        countNumber(add, count, True)
        # 进行比较
        if cmp(base, count):
            return i
    return -1
result()