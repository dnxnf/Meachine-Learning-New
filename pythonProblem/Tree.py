#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project  ：MachineLearning 
@File     ：Tree.py
@Describe ：PyCharm 
@Author   ：Hello World
@Date     ：2025/5/27 下午7:48
现有两组字母，分别表示后序遍历（左孩子->右孩子->父节点）和中序遍历（左孩子->父节点->右孩子）的结果，请你输出层序遍历的结果
input:CBEFDA CBAEDF
output:ABDCEF
'''

from collections import deque


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def build_tree(inorder, postorder):
    if not inorder or not postorder:
        return None
    root_val = postorder[-1]
    root = TreeNode(root_val)
    root_pos = inorder.index(root_val)

    root.left = build_tree(inorder[:root_pos], postorder[:root_pos])
    root.right = build_tree(inorder[root_pos + 1:], postorder[root_pos:-1])
    return root


def level_order_traversal(root):
    if not root:
        return []
    queue = deque([root])
    result = []
    while queue:
        node = queue.popleft()
        result.append(node.val)
        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)
    return result


# 输入处理
postorder, inorder = input().split()
root = build_tree(inorder, postorder)
level_order = level_order_traversal(root)
print(''.join(level_order))