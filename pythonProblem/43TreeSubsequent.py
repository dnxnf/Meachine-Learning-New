#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project  ：MachineLearning 
@File     ：43TreeSubsequent.py
@Describe ：PyCharm 
@Author   ：Hello World
@Date     ：2025/5/28 下午12:03
给定一个以顺序储存结构存储整数值的完全二叉树序列（最多1000个整数），请找出此完全二叉树的所有非叶子节点部分，
然后采用后序遍历方式将此部分树（不包含叶子）输出。
1、只有一个节点的树，此节点认定为根节点（非叶子）。
2、此完全二叉树并非满二叉树，可能存在倒数第二层出现叶子或者无右叶子的情况
其他说明：二叉树的后序遍历是基于根来说的，遍历顺序为：左-右-根
输入描述
一个通过空格分割的整数序列字符串
输出描述
后续遍历输出非叶子部分树结构
eg:
1 2 3 4 5 6 7
out:2 3 1
'''

arr = list(map(int, input().split()))
print(arr)


def dfs(arr, root, res):
    left = root * 2 + 1
    right = root * 2 + 2
    if len(arr) > left:
        dfs(arr, left, res)
        if len(arr) > right:
            dfs(arr, right, res)
        res.append(arr[root])


def result():
    if len(arr) == 1:
        return arr[0]
    res = []
    dfs(arr, 0, res)
    return " ".join(map(str, res))


result()
