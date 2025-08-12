#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project  ：MachineLearning 
@File     ：05ColorUndirectedGraphs.py
@Describe ：PyCharm 
@Author   ：Hello World
@Date     ：2025/5/27 下午9:42
给一个无向图染色，可以填红黑两种颜色，必须保证相邻两个节点不能同时为红色，输出有多少种不同的染色方案?
输入描述
第一行输入M(图中节点数)N(边数)
后续N行格式为:V1 V2表示一个V1到V2的边
数据范围:1<=M<=15,0=N=M3，不能保证所有节点都是连通的
输出描述
输出一个数字表示染色方案的个数
4 4
1 2
2 4
3 4
1 3
输出：7
'''
m, n = map(int, input().split())
arr = [list(map(int, input().split())) for i in range(n)]
# print(m, n)
# print(arr)
def result(arr, m):
    '''
    arr: 边，即[v1, v2]
    m: 点数量
    return: 染色方案数
    '''
    # connect 用于存放每个节点的相邻节点
    connect = {}
    for v1, v2 in arr:
        if connect.get(v1) is None:
            connect[v1] = set()
        connect[v1].add(v2)
        if connect.get(v2) is None:
            connect[v2] = set()
        connect[v2].add(v1)
    # 这里count是要从1开始，因为全黑是一种方案。
    # 题目说的是相邻两点不能同时为红色也就是说可以同时为黑色。
    print(f"connect:{connect}")
    return dfs(m, 1, [], 1, connect)

def dfs(m, index, path, count, connect):
    '''
    m: 点数量，点从 1 计数
    index: 当前第几个点
    path: path记录的是染红点，如果m个点都不相连，就有len(path) == m了。
    count: 染色方案数量
    connect: 每个节点的相邻节点
    return: 染色方案数量
    '''
    # 回溯第一步就是终止条件，
    if len(path) == m:
        return count
    flag = False
    # 反正你要染满m个，所以是m+1
    for i in range(index, m+1):
        # 遍历path里的节点。
        for p in path:
            if i in p:
                flag =True
                break # 结束本轮循环。就是不遍历path了。
        if flag:
            flag = False
            continue # 结束掉本次循环，使得i+1
        count += 1 # 只要染红一个就可以了。
        # 本题有句话，就是不能保证所有的是连通的
        if connect.get(i) is not None:
            path.append(connect.get(i))
            count = dfs(m, i+1, path, count, connect)
            path.pop() # 回溯
        else:
            # 假设其中一个没连通connect.get(i)就是none 那就直接递归下去不用回溯了。
            count = dfs(m, i+1, path, count, connect)
    return count
print(result(arr, m))
