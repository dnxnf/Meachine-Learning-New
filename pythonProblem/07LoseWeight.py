#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project  ：MachineLearning 
@File     ：07LoseWeight.py
@Describe ：PyCharm 
@Author   ：Hello World
@Date     ：2025/5/27 下午9:48
小明有n个可选运动，每个运动对应一个卡路里值。他需要从中选出k个运动.
使得这些运动的卡路里总和恰好为t。给定n、k、t及每个运动的卡路里列表，求可行的方案数量。
输入描述
第一行输入三个整数：n（运动数量，0 < n < 10）、t（目标卡路里总和，t > 0）、k（需选的运动数，0 < k ≤ n）。
第二行输入n个正整数，表示每个运动的卡路里值（均 > 0），以空格分隔。
输出描述
输出满足条件的方案数量（整数）。
示例
输入：
4 3 2
1 1 2 3
输出：
2
'''
def count_combinations(calories, k, t):
    n = len(calories)
    result = 0

    def backtrack(start, count, current_sum):
        nonlocal result
        if count == k and current_sum == t:
            result += 1
            return
        if count >= k or current_sum >= t:
            return
        for i in range(start, n):
            backtrack(i + 1, count + 1, current_sum + calories[i])

    backtrack(0, 0, 0)
    return result

n, t, k = map(int, input().split())
calories = list(map(int, input().split()))
print(count_combinations(calories, k, t))