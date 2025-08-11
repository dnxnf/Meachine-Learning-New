#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project  ：MachineLearning 
@File     ：40FindMaxMine.py
@Describe ：PyCharm 
@Author   ：Hello World
@Date     ：2025/5/28 上午11:44
给你一个由'0'(空地)、'1'(银矿)、'2'金矿)组成的的地图，矿堆只能由上下左右相邻的金矿或银矿连接形成。
超出地图范围可以认为是空地。假设银矿价值1，金矿价值2，请你找出地图中最大价值的矿堆并输出该矿堆的价值.
输入描述
地图元素信息如:
22220
00000
00000
11111
输出描述
矿堆的最大价值
样例
输入
22220
00000
00000
01111
输出
8
'''
directs = ((1, 0), (-1, 0), (0, -1), (0, 1))


def dfs(i, j, matrix, row, col):
    # 注意啊，这里matrix是重新传参一份了，跟原来的matrix没有关系了哈。
    total = matrix[i][j]
    matrix[i][j] = 0  # 该矿被挖了，所以置为0
    # 把他加入栈
    st = [[i, j]]
    while len(st) > 0:
        x, y = st.pop()
        for dirx, diry in directs:
            newX = x + dirx
            newY = y + diry
            # 判断边界条件是否越界, 并且要有矿啊(>0)
            if row > newX >= 0 and col > newY >= 0 and matrix[newX][newY] > 0:
                total += matrix[newX][newY]
                matrix[newX][newY] = 0  # 把矿挖了，要变成空地啊
                st.append([newX, newY])
    return total


def result(matrix):
    row = len(matrix)
    if row == 0:
        return 0
    col = len(matrix[0])
    ans = 0
    # 遍历矩阵。
    for i in range(row):
        for j in range(col):
            # 如果存在矿,开始深搜
            if matrix[i][j] > 0:  # 存在矿。
                ans = max(ans, dfs(i, j, matrix, row, col))
    return ans


# 注意这个写法。应该多谢几遍。
matrix = []
# 22220
# 00000
# 00000
# 01111
while True:
    line = input()
    # 由于本行没有说明输入的截止条件，使用空行作为截止条件。
    if line == "":
        print(result(matrix))
        break
    else:
        matrix.append(list(map(int, list(line))))