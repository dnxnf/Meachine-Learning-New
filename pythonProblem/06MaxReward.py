#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project  ：MachineLearning 
@File     ：06MaxReward.py
@Describe ：PyCharm 
@Author   ：Hello World
@Date     ：2025/5/27 下午9:45
小明每周上班都会拿到自己的工作清单，工作清单内包含n项工作，每项工作都有对应的
耗时时间(单位h)和报酬，工作的总报酬为所有已完成工作的报酬之和，那么请你帮小明安
排一下工作，保证小明在指定的工作时间内工作收入最大化。
输入描述
输入的第一行为两个正整数T，n
T代表工作时长(单位h，0<T<1000000)，
n代表工作数量(1<n<=3000)
接下来是n行，每行包含两个整数t，w
t代表该工作消耗的时长(单位h，t>0)，w代表该项工作的报酬
输出描述
输出小明指定工作时长内工作可获得的最大报酬
输入
40 3
20 10
20 20
20 5
输出
30
'''
bagweight, n=map(int, input().split())
weight = []
value = []
for i in range(n):
    w, v = map(int, input().split())
    weight.append(w)
    value.append(v)

dp = [0] * (bagweight+1)
# 先遍历物品
for i in range(len(weight)):
    # 在遍历背包
    for j in range(bagweight, weight[i]-1, -1):
        dp[j] = max(dp[j], dp[j-weight[i]]+value[i])
print(dp[bagweight])