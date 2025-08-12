#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project  ：MachineLearning 
@File     ：34PrimeMate.py
@Describe ：PyCharm 
@Author   ：Hello World
@Date     ：2025/5/28 上午11:00
定义两个正整数 a 和 b是“素数伴侣”，当且仅当 a+b 是一个素数。现在，密码学会邀请你设计一个程序，
从给定的 n个正整数{a1,a2,...,an}中，挑选出最多的“素数伴侣”，你只需要输出挑选出的“素数伴侣”对数。保证 n为偶数，一个数字只能使用一次。
输入描述
第一行输入一个正偶数 n(2≤n≤100)代表数字个数。
第二行输入 n个正整数 a1,a2,...,an(1≤ai≤3×10^4)代表给定的数字。
数据可能有多组
输出描述
输出一个整数，代表最多可以挑选出的“素数伴侣”的数量。
示例：
输入：
4
2 5 6 13
2
3 6
输出：
2
0
'''
import sys
import math


def sieve(max_num):
    is_prime = [True] * (max_num + 1)
    is_prime[0] = is_prime[1] = False
    for num in range(2, int(math.sqrt(max_num)) + 1):
        if is_prime[num]:
            is_prime[num * num: max_num + 1: num] = [False] * len(is_prime[num * num: max_num + 1: num])
    return is_prime


max_possible_sum = 60000
is_prime = sieve(max_possible_sum)


def max_prime_pairs(numbers):
    evens = []
    odds = []
    for num in numbers:
        if num % 2 == 0:
            evens.append(num)
        else:
            odds.append(num)

    graph = [[] for _ in range(len(odds))]
    for i in range(len(odds)):
        for j in range(len(evens)):
            if is_prime[odds[i] + evens[j]]:
                graph[i].append(j)

    def bpm(u, seen, match_to):
        for v in graph[u]:
            if not seen[v]:
                seen[v] = True
                if match_to[v] == -1 or bpm(match_to[v], seen, match_to):
                    match_to[v] = u
                    return True
        return False

    match_to = [-1] * len(evens)
    result = 0
    for i in range(len(odds)):
        seen = [False] * len(evens)
        if bpm(i, seen, match_to):
            result += 1
    return result


n = int(input())
numbers = list(map(int, input().split()))
print(max_prime_pairs(numbers))
