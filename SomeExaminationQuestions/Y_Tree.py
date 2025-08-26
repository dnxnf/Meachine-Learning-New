#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project     ：MachineLearning 
@File        ：Y_Tree.py
@Description ：
@Author      ：Hello World
@Date        ：2025/6/3 下午7:52
给定n 个相同的顶点，若将它们构成一棵树，且恰好存在一个顶点的度为3,其余顶点组成三条链状分支,则称这是一棵Y树。
对于两棵Y树,如果它们的三条链状分支的顶点数量完全相同，则称它们是相同的。
请计算可构建的不同Y树的数量。由于答案可能很大,请将答案对(10^9 + 7)取模后输出。
注：与一个顶点相连接的边的条数称为该顶点的度。
eg:
4
out:1
---------
6
out:2
'''
num = int(input())
if num <= 3:
    print(0)
m = num - 1
count = (m * m + 6) // 12
print(count % 1000000007)
# elif num == 4:
#     print(1)

# 剩下的情况，a，b，c分别为三条链的顶点数量
# a+b+c = num-1,从小到大排列
#
# note -------------------
# abc同一组数字算一个，121和112算一样
# for a in range(1, max_a + 1):
#     tep1 = num - 1 - a
#     min_b = a
#     max_b = tep1 // 2
#     for b in range(a, tep1 // 2 + 1):
#         c = tep1 - b
#         if c >= b and [a, b, c] not in res:
#             count += 1
#             res.append(set([a, b, c]))
#             print(a, b, c)
#
# print(count % MOD)
