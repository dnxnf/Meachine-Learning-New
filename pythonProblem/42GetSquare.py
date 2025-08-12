#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project  ：MachineLearning 
@File     ：42GetSquare.py
@Describe ：PyCharm 
@Author   ：Hello World
@Date     ：2025/5/28 上午11:57
题目描述
输入N个互不相同的二维整数坐标，求这N个坐标可以构成的正方形数量。[内积为零的的两个向量垂直]
输入描述
第一行输入为N，N代表坐标数量，N为正整数。N<=100之后的K行输入为坐标xy以空格分隔，x，y为整数，-10<=x,y<=10
输出描述
输出可以构成的正方形数量。
eg:
3
1 3
2 4
3 1
out:0 (3个点不足以构成正方形)
--------------------
4
0 0
1 2
3 1
2 -1
out:1
'''
n = int(input())
'''
4
0 0
1 2
3 1
2 -1

'''
arr = [list(map(int, input().split())) for i in range(n)]
print(arr)
def isSquare(a, b, c, d):
    points = [a, b, c, d]
    ans = set()
    for i in range(3):
        for j in range(i+1, 4):
            x, y = points[i][0] - points[j][0], points[i][1] - points[j][1]
            ans.add(x**2 + y**2)
    # 只有两种长度，1是边长，2是对角线。 并且，两种长度不能为0。如果是菱形，对角线长度绝对不一样长。
    return True if len(ans)==2 and 0 not in ans else False

def result():
    cnt = 0
    # 至少4个点啊。
    if n>3:
        for i in range(n-3):
            for j in range(i+1,n-2):
                for k in range(j+1, n-1):
                    for l in range(k+1, n):
                        if isSquare(arr[i],arr[j],arr[k],arr[l]):
                            cnt += 1
    print(cnt)
result()