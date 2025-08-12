#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project  ：MachineLearning 
@File     ：33FindSingleArea.py
@Describe ：PyCharm 
@Author   ：Hello World
@Date     ：2025/5/28 上午10:56
给定一个mxn的矩阵，由若干字符'X'和'O'构成，'X'表示该处已被占据，'O'表示该处空闲，请找到最大的单入口空闲区域
解释:
空闲区域是由连通的'O'组成的区域，位于边界的'O'可以构成入口.
单入口空闲区域即有且只有一个位于边界的'O'作为入口由连通的'O'组成的区域.若两个元素在水平或垂直方向相邻，则称它们是“连通”的
输入描述
第一行输入为两个数字，第一个数字为行数m，第二个数字为列数n，两个数字以空格分隔，
1<=m,n<=200.
剩余各行为矩阵各行元素，元素为'X'或'O'，各元素间以空格分隔
输出描述
若有唯一符合要求的最大单入口空闲区域，输出三个数字
第一个数字为入口行坐标(0~m-1)
第二个数字为入口列坐标(0~n-1)
第三个数字为区域大小
三个数字以空格分隔;
若有多个符合要求，则输出区域大小最大的，若多个符合要求的单入口区域的区域大小相同，则此时只需要输出区域大小，不需要输出入口坐标
若没有，输出NULL
eg:
4 4
X X X X
X O O X
X O O X
X O X X
out:3 1 5
'''
m, n = map(int, input().split())  # m为行数，n为列数
matrix = [list(map(str, input().split())) for i in range(m)]
print(m, n)
print(matrix)


def result(matrix, m, n):
    check = set()  # 记录检查过的,这里check是本函数的变量。对dfs函数起作用。而不是传参的方式
    directs = ((-1, 0), (1, 0), (0, -1), (0, 1))

    def dfs(i, j, count, out):
        pos = f"{i}-{j}"  # 比如1-0 和0-1表示不同的位置啦。
        # 情况1 i 或者j超界了，或者遇到了X，或者已经访问过了。结束当前深度搜索
        if i < 0 or i >= m or j < 0 or j >= n or matrix[i][j] == "X" or pos in check:
            return count
        check.add(pos)  # 访问过的要加入check中。
        # 情况2 点刚好在边缘上，
        if i == 0 or i == m - 1 or j == 0 or j == n - 1:
            out.append([i, j])  # 刚刚好在边界上，也就是入口
        # 没有超界，也不是X，pos不在check里，那么区域就要增大啊，所以count就要加1
        count += 1
        # 开始深度搜索咯
        for dirx, diry in directs:
            new_i = i + dirx
            new_j = j + diry
            count = dfs(new_i, new_j, count, out)
        return count

    ans = []
    for i in range(m):
        for j in range(n):
            if matrix[i][j] == "O" and f"{i}-{j}" not in check:
                out = []
                # 这个out是传参的形式，不同点对应的out是不一样的。
                count = dfs(i, j, 0, out)
                if len(out) == 1:
                    # 题目说了只能取入口只有一个的。多个入口的直接过滤了。
                    tmp = out[0][:]  # 这个是入口的i,j #这个切片没意义。
                    tmp.append(count)  # 然后把计数加进来。形成了[i,j,count]
                    ans.append(tmp)
    if len(ans) == 0:
        return "NULL"
    ans.sort(key=lambda x: -x[2])  # 按照区域倒序排列。
    # 若有唯一符合要求的最大单入口空闲区域，输出三个数字
    if len(ans) == 1 or ans[0][2] > ans[1][2]:  # 若有多个符合要求，则输出区域大小最大的
        return " ".join(map(str, ans[0]))
    else:  # 若多个符合要求的单入口区域的区域大小相同 ans[0][2] = ans[1][2]
        return ans[0][2]


# 算法调用
print(result(matrix, m, n))
