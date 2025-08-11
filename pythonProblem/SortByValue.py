#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project  ：MachineLearning 
@File     ：SortByValue.py
@Describe ：PyCharm 
@Author   ：Hello World
@Date     ：2025/5/28 下午5:18
根据输入的排序方式，按照成绩升序或降序输出所有学生的姓名和成绩。对于每一名学生，新起一行。
输出学生的姓名和成绩，用空格分隔。
第一行输入一个整数 n (1 ≤ n ≤ 200)代表学生人数。
第二行输入一个整数 op (0 ≤ op ≤ 1) 代表排序方式，其中，0 表示按成绩降序，1 表示按成绩升序。
此后 n 行，第i行依次输入：
一个长度为 1 ≤ len(si) ≤20、由大小写字母构成的字符串 si代表第 i 个学生的姓名；一个整数 a代表这个学生的成绩。
eg:
3
0
fang 90
yang 50
ning 70
out:
fang 90
ning 70
yang 50
'''
# 不能用字典，因为字典的键值要求唯一
n = int(input())
op = int(input())
pairs = []

for _ in range(n):
    key, value = input().split()
    pairs.append((key, int(value)))
# print(pairs)
if op == 1:
    # 根据字典的值进行排序，降序
    sorted_pairs = sorted(pairs, key=lambda x: x[1])
    for k, v in sorted_pairs:
        print(k, v)
elif op == 0:
    # 根据字典的值进行排序，升序
    sorted_pairs = sorted(pairs, key=lambda x: x[1],reverse=True)
    for k, v in sorted_pairs:
        print(k, v)