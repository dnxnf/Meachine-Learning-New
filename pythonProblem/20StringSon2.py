#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project  ：MachineLearning 
@File     ：20StringSon2.py
@Describe ：PyCharm 
@Author   ：Hello World
@Date     ：2025/5/28 上午9:44
给定字符串target和source，判断target是否为source的子序列。你可以认为target和source中仅包含英文小写字母
字符串source可能会很长(长度~=500,000)，而target是个短字符串(长度<=100)。字符串的一个子序列是原始字符串删除一些
(也可以不删除)字符而不改变剩余字符相对位置形成的新字符串。
(例如，”abc是”aebycd”的一个子序列，而”ayb”不是)
请找出最后一个子序列的起始位置。
输入描述
第一行为target，短字符串(长度<=100)第二行为source，长字符串(长度~=500.000)
输出描述
最后一个子序列的起始位置，即最后一个子序列首字母的下标
用例:
abc
abcaybec
out:3
'''
target = input()
source = input()
print(target)
print(source)
def result():
    i = len(target)-1
    j = len(source)-1
    while i >= 0:
        if target[i] == source[j]:
            i -= 1
        j -= 1
    return j+1 # 因为上一个循环已经减去1了。
print(result())
