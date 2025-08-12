#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project  ：MachineLearning 
@File     ：13NumpyNotOne.py
@Describe ：PyCharm 
@Author   ：Hello World
@Date     ：2025/5/28 上午9:26
题目描述
存在一个m*n的二维数组，其成员取值范围为0,1,2。
其中值为1的元素具备同化特性，每经过1S,将上下左右值为0的元素同化为1。而值为2的元素，免疫同化。
将数组所有成员随机初始化为0或2,再将矩阵的[0,0]元素修改成1,
在经过足够长的时间后求矩阵中有多少个元素是0或2(即0和2数量之和)。
输入描述
输入的前两个数字是矩阵大小。后面是数字矩阵内容。
输出描述
返回矩阵中非1的元素个数。
用例
输入
4 4
0000
0222
0200
0200
输出
9
说明
输入数字前两个数字是矩阵大小。后面的数字是矩阵内容。起始位置(0,0)被修改为1后，最终只能同化矩阵为：
1111
1222
1200
1200
所以矩阵中非1的元素个数为9
'''
m, n = map(int, input().split()) # m是行，n是列
arr = [list(map(int, input().split())) for i in range(m)]
print(m, n)
print(arr)
def result(arr):
    directs = ((1,0),(-1,0),(0,-1),(0,1))
    arr[0][0] = 1
    total = m * n
    for i in range(m):
        for j in range(n):
            if arr[i][j] == 1:
                total -= 1
                # print(total)
                for dirx, diry in directs:
                    new_x = i + dirx
                    new_y = j + diry
                    if 0<= new_x <m and 0<=new_y<n and arr[new_x][new_y] == 0:
                        arr[new_x][new_y] = 1
                        total -= 1
    return total
result(arr)