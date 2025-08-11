#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project     ：MachineLearning 
@File        ：图.py
@Description ：
@Author      ：Hello World
@Date        ：2025/6/7 下午12:15 
'''
import collections
from os import path
from typing import List


class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


# leetcd lcp07 拿链表构建邻接表
class Solution:
    def dfs_recursive(self, graph, u, visited):
        print(u, end=' ')  # 访问节点
        visited.add(u)  # 节点 u 标记其已访问

        for v in graph[u]:
            if v not in visited:  # 节点 v 未访问过
                # 深度优先搜索遍历节点
                self.dfs_recursive(graph, v, visited)

    # -------------------------------
    # leetcd 257 二叉树的所有路径
    #     输入：
    #    1
    #   / \
    #  2   3
    #   \
    #    5
    # 输出：["1->2->5", "1->3"]即到所有叶子节点的路径
    def binaryTreePaths(self, root: TreeNode) -> List[str]:
        def dfs(node, path):
            if not node.left and not node.right:  # 叶子节点
                res.append('->'.join(path))
                return
            if node.left:  # 有左子树时候
                dfs(node.left, path + [str(node.left.val)])
            if node.right:
                dfs(node.right, path + [str(node.right.val)])

        res = []
        dfs(root, [str(root.val)])
        return res

    def bfs(self, graph, u):
        visited = set()  # 使用 visited 标记访问过的节点
        queue = collections.deque([])  # 使用 queue 存放临时节点

        visited.add(u)  # 将起始节点 u 标记为已访问
        queue.append(u)  # 将起始节点 u 加入队列中

        while queue:  # 队列不为空
            u = queue.popleft()  # 取出队头节点 u
            print(u, end=' ')  # 访问节点 u
            for v in graph[u]:  # 遍历节点 u 的所有未访问邻接节点 v
                if v not in visited:  # 节点 v 未被访问
                    visited.add(v)  # 将节点 v 标记为已访问
                    queue.append(v)  # 将节点 v 加入队列中

    # leetcd 797,输出所有从节点 0 到节点 n-1 的所有路径，原题是有向无环图，此题根据有环图处理（添加visited）
    # 输入：graph = [[4,3,1],[3,2,4],[3],[4],[]]   对应每个索引与什么相连
    # 输出：[[0,4],[0,3,4],[0,1,3,4],[0,1,2,3,4],[0,1,4]]
    def allPathsSourceTarget(self, graph: List[List[int]]) -> List[List[int]]:
        n = len(graph)
        res = []

        # dfs 包括当前节点，当前路径，已访问节点
        def dfs(cur, path, visited):
            path.append(cur)
            visited.add(cur)
            if cur == n - 1:
                # note 这里是copy，否则会出现问题
                res.append(path.copy())
                # return # 不能return，因为还要继续搜索
            #   需要else，因为如果是最后一个节点，就不用继续搜索了
            else:
                for next in graph[cur]:
                    if next not in visited:
                        dfs(next, path, visited)
            # 最后的回溯会退出所有代码，代码执行完了
            path.pop()
            visited.remove(cur)

        dfs(0, [], set())
        return res


# ----------------------------------
graph = {
    "A": ["B", "C"],
    "B": ["A", "C", "D"],
    "C": ["A", "B", "D", "E"],
    "D": ["B", "C", "E", "F"],
    "E": ["C", "D"],
    "F": ["D", "G"],
    "G": []
}

# 基于递归实现的深度优先搜索
if __name__ == "__main__":
    visited = set()
    s = Solution()
    print("dfs", s.dfs_recursive(graph, "A", visited))
    print("bfs", s.bfs(graph, "A"))
    print("dfs，从初始节点到末尾节点的路径", s.allPathsSourceTarget([[4, 3, 1], [3, 2, 4], [3], [4], []]))
    # a = int(input(''))
    # b = int(input(''))
