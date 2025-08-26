#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project  ：MachineLearning 
@File     ：MatrixMul.py
@Describe ：PyCharm 
@Author   ：Hello World
@Date     ：2025/5/28 下午5:31
描述
如果A是个x行y列的矩阵，B是个y行z列的矩阵，把A和B相乘，其结果将是另一个x行z列的矩阵C。这个矩阵的每个元素是由下面的公式决定的

矩阵的大小不超过100*100
输入描述：
输入包含多组数据，每组数据包含：
第一行包含一个正整数x，代表第一个矩阵的行数
第二行包含一个正整数y，代表第一个矩阵的列数和第二个矩阵的行数
第三行包含一个正整数z，代表第二个矩阵的列数
之后x行，每行y个整数，代表第一个矩阵的值
之后y行，每行z个整数，代表第二个矩阵的值

输出描述：
对于每组输入数据，输出x行，每行z个整数，代表两个矩阵相乘的结果
示例1
输入：
2
3
2
1 2 3
3 2 1
1 2
2 1
3 3
复制
输出：
14 13
10 11
复制
说明：
1 2 3
3 2 1
乘以
1 2
2 1
3 3
等于
14 13
10 11

'''
# NB, 一次性通过。
# 注意点：输入矩阵的建立，行录入的时候还是要注意末尾空格，直接用input().split()分隔，就可以把空格去掉了，直接用map(int, )，不用单独去处理末尾空格。
# 如果用input().split(' '),则末尾的空格会被分隔成一个‘’字符，没法直接map(int,)


x = int(input())
y = int(input())
z = int(input())
A = []
B = []
for i in range(x):
    A.append(list(map(int, input().split())))
for j in range(y):
    B.append(list(map(int, input().split())))
# 输入录入后，开始计算，先初始化一个二维数组，初始值为0
R = [[0 for k in range(z)] for i in range(x)]
for i in range(x):
    for k in range(z):
        for j in range(y):  # 计算每个输出单元格的数据，A行与B列的乘积，长度为y
            R[i][k] += A[i][j] * B[j][k]
# 按行输出
for i in range(x):
    for k in range(z):
        print(R[i][k], end=' ')
    print('')
