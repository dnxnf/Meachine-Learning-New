#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project  ：MachineLearning 
@File     ：47WorstProduciton.py
@Describe ：PyCharm 
@Author   ：Hello World
@Date     ：2025/5/28 下午12:16
题目描述
A公司准备对他下面的N个产品评选最差奖
评选的方式是首先对每个产品进行评分，然后根据评分区间计算相邻几个产品中最差的产品。
评选的标准是依次找到从当前产品开始前M个产品中最差的产品，请给出最差产品的评分序列。
输入描述
第一行，数字M，表示评分区间的长度，取值范围是0<M<10000
第二行，产品的评分序列，
比如[12,3,8.6,5]，产品数量N范围是-10000<N<10000
输出描述
评分区间内最差产品的评分序列
eg:
3
12,3,8,6,5
out:
3,3,5
'''
n = int(input())
arr = list(map(int, input().split(",")))
print(n)
print(arr)


def result(arr, n):
    # 先把最小值初始化
    minV = min(arr[:n])  # 注意取数的时候是左闭右开，从0开始。
    ans = [minV]  # 先初始化ans
    j = n
    while j < len(arr):
        if arr[j - n] > minV:
            minV = min(minV, arr[j])
        else:
            if arr[j] <= minV:
                minV = arr[j]
            else:
                minV = min(arr[j - n + 1:j + 1])
        ans.append(minV)
        j += 1
    return ",".join(map(str, ans))


result(arr, n)
