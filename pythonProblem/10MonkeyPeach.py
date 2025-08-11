#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project  ：MachineLearning 
@File     ：10MonkeyPeach.py
@Describe ：PyCharm 
@Author   ：Hello World
@Date     ：2025/5/28 上午9:17
孙悟空爱吃蟠桃，有一天趁着蟠桃园守卫不在来偷吃。已知蟠桃园有 N 棵桃树，每颗树上都有桃子，守卫将在 H 小时后回来。
孙悟空可以决定他吃蟠桃的速度K（个/小时），每个小时选一颗桃树，并从树上吃掉 K 个，如果树上的桃子少于 K 个，则全部吃掉，
并且这一小时剩余的时间里不再吃桃。孙悟空喜欢慢慢吃，但又想在守卫回来前吃完桃子。
请返回孙悟空可以在 H 小时内吃掉所有桃子的最小速度 K（K为整数）。如果以任何速度都吃不完所有桃子，则返回0。
输入描述
第一行输入为 N 个数字，N 表示桃树的数量，这 N 个数字表示每颗桃树上蟠桃的数量。
第二行输入为一个数字，表示守卫离开的时间 H。
其中数字通过空格分割，N、H为正整数，每颗树上都有蟠桃，且 0 < N < 10000，0 < H < 10000。
输出描述
吃掉所有蟠桃的最小速度 K，无解或输入异常时输出 0。
eg
2 3 4 5
4
out:5
--------
30 11 23 4 20
6
out:23
'''
w = list(map(int, input().split()))  # 读入n个数字
h = int(input())
n = len(w)
if n > h:  # 每小时最多只能吃一颗桃树，因此没办法吃完所有桃树
    print(0)
else:
    def check(x):  # 判断当吃的速度为x的时候，是否能吃完所有桃树
        cnt = 0  # 记录吃完所有桃树的时间
        for num in w:
            cnt += (num + x - 1) // x  # 吃掉数量为num的一颗桃树所需要的时间
            if cnt > h:
                return False
        return True


    l, r = 1, 10 ** 9  # 二分左右边界
    while l < r:
        mid = l + r >> 1
        if check(mid):
            r = mid
        else:
            l = mid + 1
    print(l)

