#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project  ：MachineLearning 
@File     ：15MinNum.py
@Describe ：PyCharm 
@Author   ：Hello World
@Date     ：2025/5/28 上午9:32
给定一个整型数组，请从该数组中选择3个元素组成最小数字并输出（如果数组长度小于3，则选择数组中所有元素来组成最小数字）。
输入描述：
一行用半角逗号分割的字符串记录的整型数组，0 < 数组长度 <= 100，0 < 整数的取值范围 <= 10000。
输出描述：
由3个元素组成的最小数字，如果数组长度小于3，则选择数组中所有元素来组成最小数字。
eg:
21,30,62,5,31
输出
21305
'''
def solve():
    # 从标准输入读取数据
    arr = input().split(",")
    n = len(arr)

    # 只有一个元素时，直接输出
    if n == 1:
        print(arr[0])
    # 如果有两个元素，则比较两种组合，输出最小值
    elif n == 2:
        s1, s2 = arr[0], arr[1]
        print(min(int(s1 + s2), int(s2 + s1)))
    else:
        # 三个元素的全排列组合，找到最小值
        result = float('inf')  # 设置初始值为无穷大
        for i in range(n):
            for j in range(n):
                if i == j:
                    continue
                for k in range(n):
                    if i == k or j == k:
                        continue

                    # 将三个数字组合成一个字符串，再转化为整数进行比较
                    s = arr[i] + arr[j] + arr[k]
                    result = min(result, int(s))

        # 输出最终的最小值结果
        print(result)


if __name__ == "__main__":
    solve()

