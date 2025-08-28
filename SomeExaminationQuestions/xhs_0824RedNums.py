#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project     ：MachineLearning
@File        ：xhs_RedNums.py
@Description ：
小红是小红书的用户行为分析师。平台将每次用户行为映射为一个
正整数权重序列(a,a2a),以便后续关联推荐时提取关键“红色”行为。
为了保证标记的行为具有足够的共性,必须选出的所有“红色”行
为权重的最大公约数大于1；同时,为了避免相邻行为产生冗余,所选下标不得相邻。
现给定用户的一次行为序列,求最多可以染成红色的行为数量。
【名词解释】
最大公约数:指一组整数共有约数中最大的一个。
例如, 12,18和30的公约数有 1,2,3,6,其中最大的约数是6,因此gcd(12,18,30)=6.
in: 5
    1 2 3 2 6
out:2
@Author      ：Hello World
@Date        ：2025/8/24 下午7:44
"""
from math import gcd


# from fractions import gcd
# 解析思路：从所有公约数入手1到100，对于每个公约数遍历数组，记录最大的长度
# 之前想着是用动态规划，但是需要记录每个公约数的最大长度，而且不同的组合对应不同的公约数，
# 所以不如直接一个公约数看完，然后再看下一个公约数，这样可以减少计算量。
def solve_right(n: int, nums: list[int]) -> int:
    """
    计算最多可以染成红色的行为数量
    通过遍历所有可能的公约数(1-100)，对于每个公约数检查能被其整除的元素，
    采用贪心策略选择不相邻的元素，记录最大数量
    Args:
        n: 行为序列的长度
        nums: 用户行为权重序列
    Returns:
        int: 最多可以染成红色的行为数量
    """
    maxn = 0  # 记录最大红色行为数量

    # 遍历所有可能的公约数(1-100)
    for a in range(1, 101):
        count = 0  # 当前公约数a下能染红的数量
        j = 0  # 数组遍历指针

        # 遍历整个数组，选择能被a整除且不相邻的元素
        while j <= n:
            if nums[j] % a == 0:  # 当前元素能被a整除
                count += 1  # 计数加1
                j += 2  # 跳过下一个元素(不相邻)
            else:
                j += 1  # 继续检查下一个元素
        # 更新最大红色行为数量
        maxn = max(maxn, count)
    return maxn


# 不能连续，并且最大公约数大于1的数量
def solve(n: int, nums: list[int]) -> int:
    # o(n^2)
    dp = [[1] * n for _ in range(n)]
    # dp[i][j] 表示从i到j的数量
    # gcd_num = [1] * n # 记录到i的最大公约数
    for i in range(n):
        for j in range(i):
            if nums[i] % nums[j] == 0:
                dp[i][j] = dp[j][i] = 0  # 不能连续
            else:
                dp[i][j] = dp[j][i] = 1  # 可以连续
    count = 0
    for i in range(n):
        for j in range(i):
            if dp[i][j] == 1:
                count += 1
    return count


def solve2(n: int, nums: list[int]) -> int:
    maxn = 0

    def backtrack(start: int, end: int, count: int) -> int:
        nonlocal maxn
        if start == end:
            if count > 1:
                maxn = max(maxn, count)
            return
        for i in range(start, end):
            if nums[i] % nums[start] == 0:
                continue
            if i > start and nums[i] % nums[i - 1] == 0:
                continue
            backtrack(start + 1, i, count + 1)
            backtrack(i + 1, end, 1)

    backtrack(0, n, 1)
    return maxn


# 获得两个数的所有公约数
def get_gcd(a: int, b: int) -> list[int]:
    res = []
    for i in range(1, min(a, b) + 1):
        if a % i == 0 and b % i == 0:
            res.append(i)
    return res


def solve3(n: int, nums: list[int]) -> int:
    dp = [1] * n  # 到i为止的满足题目的数量，
    # 需要一个数组记录所有公约数，从最小的开始一次遍历公约数
    for i in range(1, n):
        for j in range(i):
            tep = get_gcd(nums[i], nums[j])
            if len(tep) > 1 and i - j > 1:  # 有多个约数，挨个遍历
                for k in tep:
                    if k > 1:
                        dp[i] = max(dp[i], dp[j] + 1)
    return max(dp)


n = int(input())
nums = list(map(int, input().split()))
print(solve(n, nums))
