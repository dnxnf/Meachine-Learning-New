#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project  ：MachineLearning 
@File     ：37FormatSecretKey.py
@Describe ：PyCharm 
@Author   ：Hello World
@Date     ：2025/5/28 上午11:40
题目描述
给定一个非空字符串 S，其被 N 个"-"分隔成 N+1 的子串，给定正整数
要求除第一个子串外，其余的串每 K 个用"-"分隔，并将小写字母转换为大写
输入描述
正整数 K 和"-"分割的字符串，如:
2
25G3C-abc-d
输出描述
转换后的字符串
用例
4
5F3Z-2e-9-w
out:5F3Z-2E9W
'''
k = int(input())
s = input()
# k = 4
# s = "5f3z-2e-9-w"
def result(s, k):
    sArr = s.split("-")
    first = sArr[0]
    if len(sArr) == 1:
        return first
    tmp = list("".join(sArr[1:]).upper()) # 转化为大写
    for i in range(len(tmp)):
        if i%k == 0:
            tmp[i] = "-" + tmp[i]
    return first+ "".join(tmp)
print(result(s, k))