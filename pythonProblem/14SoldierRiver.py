#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project  ：MachineLearning 
@File     ：14SoldierRiver.py
@Describe ：PyCharm 
@Author   ：Hello World
@Date     ：2025/5/28 上午9:28
题目描述 一支 N 个士兵的军队正在趁夜色逃亡，途中遇到一条湍急的大河.敌军在 T 的时长后到达河面，没到过对岸的士兵都会被消灭。
现在军队只找到了 1 只小船，这船最多能同时坐上2 个士兵 1.当 1 个士兵划船过河，用时为 a[i]; 0 <= i< N 2.
当 2 个士兵坐船同时划船过河时，用时为 max(a[j],a[i])两士兵中用时最长的 3.当 2 个士兵坐船 1 个士兵划船时，
用时为 a[i]*10; a[i]为划船士兵用时。 4.如果士兵下河游泳，则会被湍急水流直接带走，算作死亡。
请帮忙给出一种解决方案，保证存活的士兵最多，且过河用时最短
输入描述 第一行: N 表示士兵数(0<N<1,000,000) 第二行: T 表示敌军到达时长(0 < T< 100,000,000)
第三行: a[o] a[1] ... a[i]... a[N- 1] a[i]表示每个士兵的过河时长。 (10 < a[i]< 100; 0<= i< N)
输出描述 第一行:”最多存活士兵数”“最短用时”
备注 1)两个士兵 同时划船时，如果划速不同则会导致船原地转圈圈:所以为保持两个士兵划速相同，则需要向划的慢的士兵看齐
 2)两个士兵坐船时，重量增加吃水加深，水的阻力增大;同样的力量划船速度会变慢;
 3)由于河水湍急大量的力用来抵消水流的阻力，所以2) 中过河用时不是a[i]*2而是a[i]* 10。
 eg:
5
43
12 13 15 20 50
out:3 40
'''
n = int(input())
t = int(input())
times = list(map(int, input().split()))
# 算法
def getmax(t1, t2):
    # 传进来的条件就是t1 < t2
    if t1*10 < t2:
        return t1 * 10
    else:
        return t2

def result(n, t, times):
    times.sort() # 上来排序下。
    # 初始化dp
    dp = [0] * n
    dp[0] = times[0]
    if dp[0]>t: # 如果时间太短，最快的都过不了就没法过了。
        return "0 0"
    dp[1] = getmax(times[0], times[1]) # 厉害。
    for i in range(2, n): # 只要是两个的都要调用下getmax
        dp[i] = min(dp[i-1]+ times[0] + getmax(times[0],times[i]), dp[i-2] + times[0] + getmax(times[i-1], times[i]) + times[1] + getmax(times[0], times[1]))
        if dp[i] > t:
            return f"{i} {dp[i-1]}" # 注意下标
    return f"{n}{dp[n-1]}"
print(result(n, t, times))