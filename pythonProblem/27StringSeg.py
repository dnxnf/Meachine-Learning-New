#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project  ：MachineLearning 
@File     ：27StringSeg.py
@Describe ：PyCharm 
@Author   ：Hello World
@Date     ：2025/5/28 上午10:20
水仙花数Ⅱ 有的标题也叫 字符串分割
题目描述
给定非空字符串s，将该字符串分割成一些子串，使每个子串的ASCII码值的和均为水仙花数
1、若分割不成功，则返回0;
2、若分割成功且分割结果不唯一，则返回-1;
3、若分割成功且分割结果唯一，则返回分割后子串的数目
输入描述
输入字符串的最大长度为200
输出描述
根据题目描述中情况，返回相应的结果。
eg:
f3@d5a8
out:-1,成功但结果不唯一。
--------------
AXdddF
out:2
'''
s = input()
''' abc f3@d5a8 AXddF '''
print(s)
# s = 'AXdddF'


def isSxh(num):
    # 水仙花数是指一个三位数，每位上数字的立方和等于该数字本身，如 371 是水仙花数，因为 371=3^3+7^3+1^3
    # 首先得是三位数
    if num < 100 or num >= 1000:
        return False
    x, y, z = map(lambda x: int(x), str(num))
    # print(x, y, z)
    return num == x ** 3 + y ** 3 + z ** 3


# print(isSxh(371))
'''
这里要想清楚。为什么能用start，end来分割。
'''


def recursive(preSum, n, start, count, res):
    if start == n:  # 收获结果
        res.append(count)
        return
    # 固定start，然后来搞定end
    for end in range(start + 1, n + 1):
        if isSxh(preSum[end] - preSum[start]):
            print("start:", start, "end:", end)
            # 递归相当于子问题求解。那有个问题，有没有重复求解呢？
            recursive(preSum, n, end, count + 1, res)


def result():
    # 将字符串转化为ASCII数组
    cArr = [ord(c) for c in s]  # s = 'AXdddF'
    # 啥叫子串，连续的字符组成的子序列称为该串的子串，要连续，所以这里不能排序了。
    print(cArr)  # [65, 88, 100, 100, 100, 70]
    n = len(cArr)
    # 搞定前缀和
    preSum = [0] * (n + 1)
    for i in range(1, n + 1):
        preSum[i] = preSum[i - 1] + cArr[i - 1]  # 别忘记错一位哈。
    # res记录成功分割的情况
    # print(preSum) # [0, 65, 153, 253, 353, 453, 523]
    res = []
    recursive(preSum, n, 0, 0, res)  # 因为preSum第一个总是0，然后来分割。
    # 分割完了按照题目一个个判断。
    # 若分割不成功，则返回0;
    if len(res) == 0:
        return 0
    # 若分割成功且分割结果唯一，则返回分割后子串的数目
    elif len(res) == 1:
        return res[0]
    # 若分割成功且分割结果不唯一，则返回-1;
    else:
        return -1


print(result())