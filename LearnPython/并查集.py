#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project     ：MachineLearning
@File        ：并查集.py
@Description ：
@Author      ：Hello World
@Date        ：2025/6/6 上午11:55
"""


# what 并查集
class UnionFind:
    def __init__(self, n):
        # fa father
        self.fa = [i for i in range(n)]

    def find(self, x):  # 返回根节点序号，不在其他的里面，那就是自己
        while self.fa[x] != x:  # 当前节点不是根节点继续找
            self.fa[x] = self.fa[self.fa[x]]  # 路径压缩,
            x = self.fa[x]
        return x

    def union(self, x, y):
        # 获得根节点
        root1 = self.find(x)
        root2 = self.find(y)
        if root1 == root2:
            return False
        # 右边的赋给左边,也就是说最后一个被加入集合的是根
        self.fa[root1] = root2

        return True
    def is_connected(self, x, y):
        return self.find(x) == self.find(y)

