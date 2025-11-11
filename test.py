#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project     ：MachineLearning
@File        ：道旅 dd爱旋转.py
@Description ：
@Author      ：Hello World
@Date        ：2025/10/13 下午8:22
'''


def rotate180(matrix):
    n = len(matrix)
    matrix = [matrix[n - 1 - i] for i in range(n)]
    matrix = [row[::-1] for row in matrix]
    return matrix


def mirror(matrix):
    n = len(matrix)
    matrix = [matrix[n - 1 - i] for i in range(n)]
    return matrix


def solve2(matrix, operations):

    rotate_count = 0  # 操作1
    mirror_count = 0  # 操作2

    for op in operations:
        if op == 1:
            rotate_count += 1
        else:  # op == 2
            mirror_count += 1

    rotate_count %= 2
    mirror_count %= 2

    if rotate_count == 1:
        matrix = rotate180(matrix)
    if mirror_count == 1:
        matrix = mirror(matrix)

    return matrix


def commit():
    n = int(input())  # 矩阵大小
    matrix = []
    for i in range(n):
        lst = list(map(int, input().split()))
        matrix.append(lst)
    q = int(input())  # 询问次数
    a = []
    for i in range(q):
        x = int(input())  # 1或者2，1代表顺时针180度，2代表行镜像
        a.append(x)

    # 使用优化版本
    res = solve2(matrix, a)

    for row in res:
        print(' '.join(map(str, row)))


if __name__ == "__main__":
    commit()