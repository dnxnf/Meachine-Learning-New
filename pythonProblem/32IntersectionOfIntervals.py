#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project  ：MachineLearning 
@File     ：32IntersectionOfIntervals.py
@Describe ：PyCharm 
@Author   ：Hello World
@Date     ：2025/5/28 上午10:53
题目描述
给定一组闭区间，其中部分区间存在交集。
任意两个给定区间的交集，称为公共区间(如:[1,2],[2,3]的公共区间为[2,2],[3,5],[3,6]的公共区间为[3,5])
公共区间之间若存在交集，则需要合并(如:[1,3],[3,5]区间存在交集[3,3],需合并为[1,5])。按升序排列输出合并后的区间列表
输入描述
组区间列表
区间数为 N: O<=N<=1000。
区间元素为 X:-10000<=X<=10000。
输出描述
升序排列的合并区间列表
备注
1、区间元素均为数字，不考虑字母、符号等异常输入。
2、单个区间认定为无公共区间。
用例
4
0 3
1 3
3 5
3 6
out:1 5
'''
n = int(input())
ranges = [list(map(int, input().split())) for  i in range(n)]
print(ranges)
def result(n, ranges):
    # 先把开始位置排序。
    ranges.sort(key = lambda x:x[0])
    combine = []
    for i in range(n):
        s1, e1 = ranges[i]
        for j in range(i+1, n):
            s2, e2 = ranges[j]
            if s2<=e1:
                combine.append([s2, min(e1, e2)]) # 因为s2绝对大于等于s1了的。
            else:
                # 这里必须是break，因为没有交集了，能结束这个循环了，后面的只可能更大了，不用计算了
                break
    if len(combine) == 0:
        print("None")
        return
    combine.sort(key= lambda x:(x[0], -x[1]))
    pre = combine[0]
    for i in range(1, len(combine)):
        cur = combine[i]
        if pre[1] >= cur[0]:
            # 前一个的end 大于现在的start
            pre[1] = max(cur[1], pre[1]) # 更新前一个的start
        else:
            print(" ".join(map(str, pre)))
            pre = cur
    print(" ".join(map(str, pre)))
result(n, ranges)