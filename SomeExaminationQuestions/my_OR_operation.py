#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         : my_OR_operation.py
@Description  :
题目重述
给定一个整数数组，我们需要选择一个非负整数 x，满足：
最高优先级：使x OR (a1 OR a2 OR... OR an)  的值尽可能小
次高优先级：在满足条件1的所有x中，选择值最大的x
输入输出样例
示例1：
输入：
3
1 2 3
输出：
3
解释：x=3时，(1|3)=3, (2|3)=3, (3|3)=3，OR结果为3，是最小的可能值。
-----------示例2：
输入：
4
5 10 15 20
输出：31
@Author       : Hello World
@Date         : 2025-09-08 09:01:59
"""

# 异或整个数组得到A，这个A就是所求的x。
# 关键思路：
# x OR S 的结果至少包含 S 的所有位（因为 OR 运算的特性）
# 要最小化 x OR S，意味着我们要让这个结果尽可能接近 S 本身
# 换句话说，x 不应该引入任何 S 中没有的位（否则 x OR S 会变大
def solve(arr):
    temp = arr[0]
    if len(arr) == 1:
        return temp
    for i in range(len(arr)-1):
        temp = temp | arr[i+1]
        # print(temp)
    return temp


def commit():
    n = int(input())
    arr = list(map(int, input().split()))
    res = solve(arr)
    print(res)

commit()