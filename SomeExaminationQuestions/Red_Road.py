#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project     ：MachineLearning 
@File        ：Red_Road.py
@Description ：
@Author      ：Hello World
@Date        ：2025/6/3 下午8:37
小红有一个n个点m条边的无向图,每条边有一个权值wi。小红现在计划修k条双向道路，起点是1号点，终点是其他顶点。
假设修了这k条路后，从1号点到其他点的距离为di,小红想知道，可以少修多少条路，使得从1号点到其他点的距离仍然为di。
输入：第一行三个整数n,m,k,表示点数,边数,以及小红计划修的路数。
接下来 m 行，每行三个整数 Ui,Ui,wi，表示一条边的两个端点以及权值。
接下来k行,每行两个整数pi,Si,表示计划修从1号点到pi号点的一条路，长度为 Si。
输出：输出一个整数，表示可以少修的路数。
eg:
2 2 2
1 2 2
2 1 3
2 2
2 3
out:2
'''


def main():
    n, m, k = map(int, input().split())
    # 初始化图
    graph = [[] for _ in range(1,n + 1)]
    for _ in range(m):
        u, v, w = map(int, input().split())
        graph[u].append((v, w))
        graph[v].append((u, w))
    # 初始化计划修的路
    plan = []
    for _ in range(k):
        p, s = map(int, input().split())
        plan.append((p, s))
    # 计算可以少修的路数
    count = 0
    for p, s in plan:
        # 从1号点到p号点的最短路
        dist = [float('inf')] * (n + 1)
        dist[1] = 0
        # 使用BFS
        queue = [1]
        while queue:
            u = queue.pop(0)
            for v, w in graph[u]:
                if dist[v] > dist[u] + w:
                    dist[v] = dist[u] + w
                    queue.append(v)
        # 判断是否可以少修一条路
        if dist[p] <= s:
            count += 1
    print(count)
main()