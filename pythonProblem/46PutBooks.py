#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project  ：MachineLearning 
@File     ：46PutBooks.py
@Describe ：PyCharm 
@Author   ：Hello World
@Date     ：2025/5/28 下午12:10
书籍叠放 最长递增子序列+二分查找
题目描述
书籍的长、宽都是整数对应(l,w)。如果书 A 的长宽度都比 B 长宽大时，则允许将 B 排列
放在 A 上面。现在有一组规格的书籍，书籍叠放时要求书籍不能做旋转，请计算最多能有
多少个规格书籍能叠放在一起。
输入描述
输入: books = [[20,16],[15,11],[10,10],[9,10]]
说明: 总共 4 本书籍，第一本长度为 20 宽度为 16;第二本书长度为 15 宽度为 11，依次
类推，最后一本书长度为 9 宽度为 10.
输出描述
输出: 3
说明: 最多 3 个规格的书籍可以叠放到一起,从下到上依次为:[20,16],[15,11,[10,10]
用例
输入 [[20,16],[15,11],[10,101],[9,10]]
输出 3
'''
books = eval(input())
def result():
    books.sort(key= lambda x:(x[0], -x[1]))
    N = len(books)
    res = 0
    dp=[1]*N
    for i in range(N):
        for j in range(i):
            # 第一维度已经是升序排列了。然后第二维度。如果是升序排列就好了
            if books[j][1]<books[i][1]:
                dp[i] = max(dp[i], dp[j]+1)
    return max(dp)
print(result())