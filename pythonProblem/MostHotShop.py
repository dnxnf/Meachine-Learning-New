#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project  ：MachineLearning 
@File     ：MostHotShop.py
@Describe ：PyCharm ,结果暂时不对
@Author   ：Hello World
@Date     ：2025/5/28 下午1:31
某购物城有m个商铺，现决定举办一场活动选出人气最高店铺。
活动共有n位市民参与，每位市民只能投一票，但1号店铺如果给该市民发放 q 元的购物补贴，该市民会改为投1号店铺。
请计算1号店铺需要最少发放多少元购物补贴才能成为人气最高店铺（即票数大于其他店铺），如果1号店铺本身就是票数最高店铺，返回0。
输入描述
第一行为小写逗号分割的两个整数n，m，其中：
第一个整数n表示参与的市民总数
第二个整数m代表店铺总数
1 ≤ n,m ≤ 3000
第2到n+1行，每行为小写逗号分割的两个整数p，q，表示市民的意向投票情况，其中每行的：
第一个整数p表示该市民意向投票给p号店铺
第二个整数q表示其改投1号店铺所需给予的q元购物补贴
1 ≤ p ≤ m
1 ≤ q ≤ 10^9
不考虑输入的格式问题
eg:
5,5
2,10
3,20
4,30
5,40
5,90
out:50
-------------
5,5
2,10
3,20
4,30
5,80
5,90
out:60
'''
import heapq


def min_shopping_subsidy():
    # 读取输入
    n, m = map(int, input().split(','))

    # 初始化每个店铺的票数和改投成本堆
    votes = {i: 0 for i in range(1, m + 1)}
    shop_queues = {}  # 每个店铺的改投成本堆（小顶堆）
    for p in range(2, m + 1):
        shop_queues[p] = []

    # 读取市民数据
    for _ in range(n):
        p, q = map(int, input().split(','))
        votes[p] += 1
        if p != 1:
            heapq.heappush(shop_queues[p], q)

    current_1 = votes[1]
    total_cost = 0

    while True:
        # 找出当前其他店铺的最大票数及其对应的店铺
        max_vote = -1
        candidates = []
        for p in range(2, m + 1):
            if votes[p] > max_vote:
                max_vote = votes[p]
                candidates = [p]
            elif votes[p] == max_vote:
                candidates.append(p)

        if current_1 > max_vote:
            print(total_cost)
            return

        if max_vote == 0:
            break  # 没有其他店铺有票

        # 选择所有可能减少max_vote的店铺中，改投成本最低的
        min_cost = float('inf')
        best_p = -1
        for p in candidates:
            if shop_queues[p]:
                current_min = shop_queues[p][0]
                if current_min < min_cost:
                    min_cost = current_min
                    best_p = p

        if best_p == -1:
            break  # 没有可改投的市民

        # 执行改投
        cost = heapq.heappop(shop_queues[best_p])
        total_cost += cost
        current_1 += 1
        votes[best_p] -= 1

    print(total_cost if current_1 > max_vote else 0)


min_shopping_subsidy()
