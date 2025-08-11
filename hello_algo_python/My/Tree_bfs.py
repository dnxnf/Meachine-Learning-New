#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project     ：MachineLearning 
@File        ：Tree_bfs.py
@Description ：
@Author      ：Hello World
@Date        ：2025/6/4 上午10:34 
'''
from collections import deque

from hello_algo_python.modules import *


# 二叉树的层次遍历
# note bfs层次一般用队列queue,深搜dfs一般用递归
def level_order(root: TreeNode) -> list[int]:
    # 队列
    queue = deque()
    queue.append(root)
    res = []
    # 队列里面还有的时候
    while queue:
        node = queue.popleft()
        res.append(node.val)  # 入队
        if node.left is not None:
            queue.append(node.left)
        if node.right is not None:
            queue.append(node.right)
    return res


if __name__ == '__main__':
    tree = list_to_tree([1, 2, 3, 4, None, 6, 7, 8, 9, None, None, 12, None, None, 15])
    print_tree(tree)
    print(level_order(tree))
