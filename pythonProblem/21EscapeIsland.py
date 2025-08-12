#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project  ：MachineLearning 
@File     ：21EscapeIsland.py
@Describe ：PyCharm 
@Author   ：Hello World
@Date     ：2025/5/28 上午9:47
有一个荒岛，只有左右两个港口，只有一座桥连接这两个港口，现在有一群人需要从两个港口逃生，有的人往右逃生，有的往左逃生.
如果两个人相遇，则PK，体力值大的能够打赢体力值小的，体力值相同则同归干尽，赢的人才能继续往前逃生，并减少相应的体力
输入描述
一行非 0 整数，用空格隔开，正数代表向右逃生，负数代表向左逃生
输出描述
最终能够逃生的人数
示例1：
输入
5 10 8 -8 -5
输出
2
说明
8与-8 相遇，同归于尽，10 遇到-5，打赢并减少五点体力，最终逃生的为5，5，均从右侧港口逃生，输出2
'''
from typing import List

def asteroidCollision(people: List[int]) -> int:
    survivors = []
    for person in people:
        if person == 0:
            return -1
        alive = True
        # 当前人向左逃生，且有人向右逃生时进行决斗
        while alive and person < 0 and survivors and survivors[-1] > 0:
            # 决斗结果：当前人战斗力大于对手
            alive = survivors[-1] < -person
             # 如果战斗力相等或当前人战斗力更大，移除对手
            if survivors[-1] <= -person:
                survivors.pop()
            else:
                alive = False
        # 如果当前人仍然存活，将其添加到逃生者列表
        if alive:
            survivors.append(person)
    return len(survivors)

try:
    # 从输入获取人员列表
    people = list(map(int, input().split()))

    # 检查输入是否异常
    if len(people) > 30000:
        raise ValueError("输入异常")

    # 调用函数并输出结果
    result = asteroidCollision(people)
    print(result)
except ValueError as e:
    print(-1)