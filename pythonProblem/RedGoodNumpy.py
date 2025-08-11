#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project     ：MachineLearning 
@File        ：RedGoodNumpy.py
@Description ：有问题，样例没过完，保留元素地方出问题了
@Author      ：Hello World
@Date        ：2025/6/3 下午7:31
小红定义了一种名为“好数组”的数组：当一个数组的大小等于其包含的元素种类数量时，
它就是一个好数组。特别地，空数组也是一个好数组。例如：
{1,2,3}是好数组(大小为3,有3种元素:1,0,2,4)。
{1,0,2,4}是好数组(大小为4,有4种元素:是好数组（大小为0，有0 种元素）。
{1,1,4,5,1,4}不是好数组（大小为6,但只有3种元素：1,4,5。6 3）。
现在,小红有一个初始数组 a。她可以对数组执行以下操作：
选择删除数组中的任意 k个元素。
这个操作可以执行任意次（也可以为零次），但每次执行前必须保证当前数组的大小至少为 k。
小红想知道，通过若干次删除操作后，她能否将初始数组 α 变成一个好数组？
每个测试文件均包含多组测试数据。第一行输入一个整数代表数据组数,每组测试数据描述如下:
第一行输入两个正整数n和k(1<n,k<100),代表小红初始数组的大小、每次操作删除的元素数量。
第二行是 n个正整数 a1,a2,..,an (1 <ai < 100)，代表初始数组的元素。
eg:
2
4 2
1 2 2 3
5 3
1 1 1 1 1
out:Yes
No
'''
group = int(input())
for _ in range(group):
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    # 判断是否是好数组,数组长度不小于k，可以执行k次操作
    if n >= k and len(set(a)) == n:
        print("Yes")
    m = len(set(a))
   # print(m)  # 元素种类数量想
    possible = False
    for i in range(m, -1, -1):
        if (n - i) % k == 0 and i <= n:
            freq = {}
            for num in a:
                freq[num] = freq.get(num, 0) + 1
            #     至少也要i个元素
            if len(freq) >= i:
                possible = True
                break
    if possible:
        print("Yes")
    else:
        print("No")
