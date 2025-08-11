#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project  ：MachineLearning 
@File     ：01Symmetry.py
@Describe ：PyCharm 
@Author   ：Hello World
@Date     ：2025/5/27 下午8:47
对称就是最大的美学，现有一道关于对称字符串的美学。已知:
第1个字符串:R
第2个字符串:BR
第3个字符串:RBBR
第4个字符串:BRRBRBBR
第5个字符串:RBBRBRRBBRRBRBBR
相信你已经发现规律了，没错!就是第个字符串=第i-1号字符串取反+第i-1号字
符串
取反(R->B，B->R)
现在告诉你n和k，让你求得第n个字符串的第k个字符是多少。(k的编号从0开始)
输入描述
第一行输入一个T，表示有T组用例;
解析来输入T行，每行输入两个数字，表示n，k
1≤T≤100;
1<n<64;
0<=k<2^(n-1);
--------
5
1 0
2 2
3 2
4 6
5 8
输出描述
red
red
blue
blue
blue
输出T行表示答案;
输出“blue"表示字符是B;
输出"red"表示字符是R。
备注:输出字符串区分大小写，请注意输出小写字符串，不带双引号。
'''
import math


def getNK(n, k):
    if n == 1:
        return "red"
    # n=2的话，k只能取0或者1
    if n == 2:
        if k == 0:
            return "blue"
        else:
            return "red"
    # 取字符的一半
    half = math.pow(2, n - 2)
    if k >= half:
        # 再后半段,就跟n-1的一样的，我们就把参数改下
        return getNK(n - 1, k - half)
    # 在前半段，就取反
    else:
        return "blue" if getNK(n - 1, k) == "red" else "red"


t = int(input())
# 注意这里需要转float,没办法，数据量特别大
# 64 73709551616
arr = [list(map(float, input().split())) for i in range(t)]


# print(arr)
def result():
    for n, k in arr:
        print(getNK(n, k))


result()
