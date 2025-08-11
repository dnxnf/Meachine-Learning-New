#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project  ：MachineLearning 
@File     ：11HappyWeekend.py
@Describe ：PyCharm 
@Author   ：Hello World
@Date     ：2025/5/28 上午9:19
小华和小为是很要好的朋友，他们约定周末一起吃饭。
通过手机交流，他们在地图上选择了多个聚餐地点(由于自然地形等原因，部分聚餐地点不可达)。
求小华和小为都能到达的聚餐地点有多少个?
输入描述
第一行输入m和n，m代表地图的长度，n代表地图的宽度
第二行开始具体输入地图信息，地图信息包含:
0 为通畅的道路
1 为障碍物 (且仅1为障碍物)
2 为小华或者小为，地图中必定有且仅有2个(非障碍物)
3 为被选中的聚餐地点 (非障碍物)
输出描述
可以被两方都到达的聚餐地点数量，行末无空格
示例1
输入：
4 4
2 1 0 3
0 1 2 1
0 3 0 0
0 0 0 0
输出：
2
说明：第一行输入地图的长宽为4，4，接下来4行是地图2表示华为的位置，3是聚餐地点，图中的两个3，小华和小为都可到达，所以输出2
示例2
输入
4 4
2 1 2 3
0 1 0 0
0 1 0 0
0 1 0 0
输出
0
'''
def dfs(g, r, c, vis, seq):
    if r < 0 or c < 0 or r >= m or c >= n or g[r][c] == 1 or ((vis[r][c] >> seq) & 1 ) == 1:
        return

    # 第 seq 个人访问(i,j) 则将 vis[i][j] 的二进制第 seq 位变为 1
    vis[r][c] |= (1 << seq)

    dfs(g, r + 1, c, vis, seq)
    dfs(g, r - 1, c, vis, seq)
    dfs(g, r, c + 1, vis, seq)
    dfs(g, r, c - 1, vis, seq)


m, n = map(int, input().split())

g = [list(map(int, input().split())) for _ in range(m)]
vis = [[0] * n for _ in range(m)]


# 起点位置（小华或者小为的位置）
starts = [(r, c) for r in range(m) for c in range(n) if g[r][c] == 2]
for seq, (r, c) in enumerate(starts):
    dfs(g, r, c, vis, seq)


result = sum(1 for r in range(m) for c in range(n) if g[r][c] == 3 and vis[r][c] == 3)
print(result)

