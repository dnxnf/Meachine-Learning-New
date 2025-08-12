#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project  ：MachineLearning 
@File     ：09AssemblyLine.py
@Describe ：PyCharm 
@Author   ：Hello World
@Date     ：2025/5/28 上午9:15
题目描述
一个工厂有 m 条流水线，来并行完成 n 个独立的作业，该工厂设置了一个调度系统，在安排作业时，总是优先执行处理时间最短的作业.
现给定流水线个数 m，需要完成的作业数 n,每个作业的处理时间分别为 t1.t2...tn。请你编程计算处理完所有作业的耗时为多少?
当 n>m 时，首先处理时间短的 m 个作业进入流水线，其他的等待，当某个作业完成时，依次从剩余作业中取处理时间最短的进入处理。
输入描述
第一行为2 个整数 (采用空格分隔)，分别表示流水线个数 m 和作业数 n;
第二行输入 n个整数 (采用空格分隔) ，表示每个作业的处理时长 t1,t2...tn。0< m,n<100，0<t1,t2...tn<100.
注: 保证输入都是合法的
输出描述
输出处理完所有作业的总时长。
eg
3 5
8 4 3 2 10
输出:13
'''
m, n = map(int, input().split())
times = list(map(int, input().split()))
print(m, n)
print(times)
def result():
    times.sort() # 升序排列
    # 初始化每条线的时间
    arr = [0] * m
    for i in range(len(times)):
        arr[i%m] += times[i] # 取余，常规做法。
    # print(arr)
    return max(arr)
print(result())