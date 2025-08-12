#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project  ：MachineLearning 
@File     ：22MoreTask.py
@Describe ：PyCharm 
@Author   ：Hello World
@Date     ：2025/5/28 上午9:54
一个应用启动时，会有多个初始化任务需要执行，并且任务之间有依赖关系，例如A任务依赖B任务，那么必须在B任务执行完成之后，
才能开始执行A任务。现在给出多条任务依赖关系的规则，请输入任务的顺序执行序列，规则采用贪婪策略，即一个任务如果没有依赖的任务，
则立刻开始执行，如果同时有多个任务要执行，则根据任务名称字母顺序排序。例如: B任务依赖A任务，C任务依赖A任务，
D任务依赖B任务和C任务，同时，D任务还依赖E任务。那么执行任务的顺序由先到后是:A任务，E任务，B任务，C任务，D任务。
这里A和E任务都是没有依赖的，立即执行。
输入描述
输入参数每个元素都表示任意两个任务之间的依赖关系，输入参数中符号”->”表示依赖方向。
例如A->B表示A依赖B，多个依赖之间用单个空格分割
输出描述
输出为排序后的启动任务列表，多个任务之间用单个空格分割
示例1
输入：
A->B C->B
输出：
B A C
'''
outdegree = dict()
depend = dict()

# 建立依赖关系，维护出度
for relation in input().split():
    # a 依赖 b
    a, b = relation.split('->')
    depend.setdefault(b, []).append(a)
    outdegree.setdefault(a, 0)
    outdegree.setdefault(b, 0)
    outdegree[a] += 1

# 拓扑排序结果
rs = []
while True:
    # 找到出度为0的节点，并将其加入结果集中
    temp = [key for key, indeg in outdegree.items() if indeg == 0]
    # 一旦出度为0的节点不存在，则退出循环
    if not temp:
        break

    temp.sort()
    for key in temp:
        rs.append(key)
        outdegree[key] = -1  # 表示已经遍历
        # 邻居节点出度 -1
        for neighbor in depend[key]:
            outdegree[neighbor] -= 1

print(" ".join(rs))

