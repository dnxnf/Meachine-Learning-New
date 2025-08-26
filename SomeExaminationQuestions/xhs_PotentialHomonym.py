#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project     ：MachineLearning 
@File        ：xhs_PotentialHomonym.py
@Description ：没写出来
在小红书平台的社交推荐项目中，产品团队希望基于用户的日常行为习惯分数，挖掘潜在的“同好”关系。
系统简化如下，数据库中有 n 个用户的日常行为习惯分数，第i个
用户的分数使用 a表示。记第i个用户和第j个用户构成“同好”关
系，当且仅当 ai能被aj整除，或者 aj能被ai整除。
接下来将进行m次查询,每次给定一个额外的用户行为分数×,请
统计在数据库中，有多少不同的人能与这个人构成“同好”关系。
输入描述
第一行输入两个整数 n,m(1≤n,m≤5×105)，表示数据库中用户数量、查询次数。
第二行输入n个整数a,,a2...a,(1sa;s5x105),表示数据库中的用户日常行为习惯分数。
接下来 m 行，每行输入一个整数 x(1<x<5×105)，表示一个额外的用户行为习惯分数。
输出描述
对于每次查询，新起一行，输出一个整数，表示数据库中能与x 构成“同好”关系的用户数量。
input:
5 3
1 2 2 5 6
4
2
1
out:
3
4
5
Explanation:
在第一次查询中，额外的用户行为习惯分数为 4，能与 4 构成“同好”关系的用户有 1、2、2，共计 3 个。
在第二次查询中，额外的用户行为习惯分数为 2，能与 2 构成“同好”关系的用户有 1、2、2、6，共计 4 个。
在第三次查询中，额外的用户行为习惯分数为 1，能与 1 构成“同好”关系的用户有 1、2、2、5、6，共计 5 个。
@Author      ：Hello World
@Date        ：2025/8/24 下午8:09 
'''

# 再把思路过一遍，对于每个额外用户，需要全都过一遍，只咬能互相整除，就加一，最后输出count,普通方法复杂度为O(nm),超时了，需要优化
# 其实考的是埃拉托斯特尼筛法，可以优化到O(nlogn+m)
from collections import defaultdict


def solve_right(nums, lst) -> list[int]:
    # 使用题目给定的最大值500000，而不是max(nums)
    MAX = max(nums)

    # 统计频率
    freq = defaultdict(int)
    for num in nums:
        if num <= MAX:
            freq[num] += 1

    # 倍数关系，F[i]记录了i的倍数的个数
    F = [0] * (MAX + 1)
    for i in range(1, MAX + 1):
        j = i
        while j <= MAX:
            F[i] += freq.get(j, 0)
            j += i

    # div记录能整除i的数的个数（即i的约数个数）
    div = [0] * (MAX + 1)
    for i in range(1, MAX + 1):
        j = i
        while j <= MAX:
            div[j] += freq.get(i, 0)
            j += i

    # 处理查询
    res = []
    for x in lst:
        if x > MAX:
            res.append(0)
        else:
            # F[x]: x的倍数出现的次数
            # div[x]: x的约数出现的次数
            # freq.get(x, 0): x本身出现的次数（减去重复计算）
            count = F[x] + div[x] - freq.get(x, 0)
            res.append(count)

    return res


def submit2():
    n, m = map(int, input().split())
    nums = list(map(int, input().split()))
    lst = []
    for i in range(m):
        x = int(input())
        lst.append(x)
    print(lst)
    res = solve_right(nums, lst)
    for i in res:
        print(i)


# 看输入的数据有和之前的几个互为倍数关系
def solve(a, x) -> int:
    # 超时了
    count = 0
    for i in a:
        if i % x == 0 or x % i == 0:
            count += 1
    return count


def solve2(nums, x) -> int:
    # 要得到的是能与x 构成“同好”关系的用户数量，所以只需要统计x能被多少个数整除即可
    count = 0
    left, right = 0, len(nums) - 1
    while left <= right:
        if nums[left] % x == 0 or x % nums[left] == 0:
            count += 1
            while nums[left] == nums[left + 1] and left < right:
                left += 1
                count += 1
        if nums[right] % x == 0 or x % nums[right] == 0:
            count += 1
            while nums[right] == nums[right - 1] and left < right:
                right -= 1
                count += 1
        left += 1
        right -= 1
    return count


def submit():
    n, m = map(int, input().split())
    nums = list(map(int, input().split()))
    nums.sort()
    for i in range(m):
        x = int(input())
        res = solve2(nums, x)
        print(res)


submit2()
