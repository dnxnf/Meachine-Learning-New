#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project  ：MachineLearning 
@File     ：41RNA_Testing.py
@Describe ：PyCharm 
@Author   ：Hello World
@Date     ：2025/5/28 上午11:54
为了达到新冠疫情精准防控的需要，为了避免全员核酸检测带来的浪费，需要精准圈定可能被感染的人群。
现在根据传染病流调以及大数据分析，得到了每个人之间在时间、空间上是否存在轨迹的交叉。
现在给定一组确诊人员编号(X1,X2,X3...Xn) 在所有人当中，找出哪些人需要进行核酸检测，输出需要进行核酸检测的人数。
（注意:确诊病例自身不需要再做核酸检测)
需要进行核酸检测的人，是病毒传播链条上的所有人员，即有可能通过确诊病例所能传播到的所有人。
例如:A是确诊病例，A和B有接触、B和C有接触 C和D有接触，D和E有接触。那么B、C、D、E都是需要进行核酸检测的
输入描述
第一行为总人数N
第二行为确诊病例人员编号 (确证病例人员数量 < N) ，用逗号隔开
接下来N行，每一行有N个数字，用逗号隔开，其中第i行的第个j数字表名编号i是否与编号j接触过。0表示没有接触，1表示有接触
输出描述
输出需要做核酸检测的人数
补充说明
人员编号从0开始
0 < N < 100
eg:
输入：
5
1,2
1,1,0,1,0
1,1,0,0,0
0,0,1,0,1
1,0,0,1,0
0,0,1,0,1
输出
3
'''


class UnionFind:
    def __init__(self, size):
        self.parent = list(range(size))

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        x_root = self.find(x)
        y_root = self.find(y)
        if x_root != y_root:
            self.parent[y_root] = x_root


def main():
    n = int(input())
    confirm = list(map(int, input().split(',')))

    uf = UnionFind(n)

    # 合并所有确诊病例
    first_case = confirm[0]
    for case in confirm[1:]:
        uf.union(first_case, case)

    # 处理接触矩阵
    for i in range(n):
        row = list(map(int, input().split(',')))
        for j in range(n):
            if row[j] == 1:
                uf.union(i, j)

    # 统计与确诊病例同一集合的人数
    target_root = uf.find(first_case)
    count = 0
    for i in range(n):
        if uf.find(i) == target_root:
            count += 1

    # 减去确诊病例自身
    print(count - len(confirm))


if __name__ == "__main__":
    main()