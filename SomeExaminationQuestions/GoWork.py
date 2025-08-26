#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project  ：MachineLearning 
@File     ：GoWork.py
@Describe ：PyCharm 
@Author   ：Hello World
@Date     ：2025/5/27 下午7:25 
'''
'''
Jungle 生活在美丽的蓝鲸城，大马路都是方方正正，但是每天马路的封闭情况都不一样。
地图由以下元素组成：
”.” — 空地，可以达到;
” * ” — 路障，不可达到;
”S” — Jungle的家;
”T” — 公司.
其中我们会限制Jungle拐弯的次数，同时Jungle可以清除给定个数的路障，现在你的任务是计算Jungle是否可以从家里出发到达公司。
输入：
输入的第一行为两个整数t,c（0 ≤ t,c ≤ 100）,t代表可以拐弯的次数，c代表可以清除的路障个数。
输入的第二行为两个整数n,m（1 ≤ n,m ≤ 100）,代表地图的大小。
接下来是n行包含m个字符的地图。n和m可能不一样大。
我们保证地图里有S和T。
输出:是否可以从家里出发到达公司，是则输出YES，不能则输出NO
示例输入：
2 0
5 5
..S..
****.
T....
****.
.....
示例输出：
YES
'''
from collections import deque
# 有问题

def solve():
    t, c = map(int, input().split())
    n, m = map(int, input().split())
    grid = [list(input().strip()) for _ in range(n)]

    # 寻找起点S的位置
    start = None
    for i in range(n):
        for j in range(m):
            if grid[i][j] == 'S':
                start = (i, j)
                break
        if start:
            break

    # 定义四个移动方向：上、下、左、右
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # 初始化访问数组，维度为 [n][m][4][t+1][c+1]
    visited = [[[[[-1 for _ in range(c + 1)] for __ in range(t + 1)]
                 for ___ in range(4)] for ____ in range(m)] for _____ in range(n)]

    q = deque()

    # 将四个方向的初始移动加入队列
    for dir_idx in range(4):
        di, dj = directions[dir_idx]
        ni, nj = start[0] + di, start[1] + dj
        if 0 <= ni < n and 0 <= nj < m:
            if grid[ni][nj] == '*':
                if c > 0:
                    q.append((ni, nj, dir_idx, 1, 1))
                    visited[ni][nj][dir_idx][1][1] = 1
            else:
                q.append((ni, nj, dir_idx, 0, 0))
                visited[ni][nj][dir_idx][0][0] = 1

    found = False
    while q:
        i, j, dir_idx, turns, cleared = q.popleft()

        # 到达终点T
        if grid[i][j] == 'T':
            found = True
            break

        # 跳过已访问的状态
        if visited[i][j][dir_idx][turns][cleared] == 1:
            continue
        visited[i][j][dir_idx][turns][cleared] = 1

        # 探索四个方向
        for new_dir_idx in range(4):
            di, dj = directions[new_dir_idx]
            ni, nj = i + di, j + dj
            if 0 <= ni < n and 0 <= nj < m:
                if grid[ni][nj] == 'T':
                    found = True
                    break
                # 处理路障
                if grid[ni][nj] == '*':
                    if cleared >= c:
                        continue  # 无法清除更多路障
                    new_cleared = cleared + 1
                    new_turns = turns + 1 if new_dir_idx != dir_idx else turns
                else:
                    new_cleared = cleared
                    new_turns = turns + 1 if new_dir_idx != dir_idx else turns

                # 检查是否超过拐弯次数限制
                if new_turns > t:
                    continue

                # 检查新状态是否已访问
                if visited[ni][nj][new_dir_idx][new_turns][new_cleared] == -1:
                    visited[ni][nj][new_dir_idx][new_turns][new_cleared] = 1
                    q.append((ni, nj, new_dir_idx, new_turns, new_cleared))
        if found:
            break

    print("YES" if found else "NO")


solve()