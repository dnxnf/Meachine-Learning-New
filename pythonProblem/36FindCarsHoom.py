#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project  ：MachineLearning 
@File     ：36FindCarsHoom.py
@Describe ：PyCharm 
@Author   ：Hello World
@Date     ：2025/5/28 上午11:36
题目描述
停车场有一横排车位，0代表没有停车，1代表有车。至少停了一辆车在车位上，也至少有一个空位没有停车为了防剐蹭，
需为停车人找到一个车位，使得距停车人的车最近的车辆的距离是最大的，返回此时的最大距离。
输入描述
1.一个用半角逗号分割的停车标识字符串，停车标识为0或1，0为空位，1为已停车。
2.停车位最多100个。
输出描述
输出一个整数记录最大距离
用例
1,0,0,0,0,1,0,0,1,0,1
out:2
'''
nums = list(map(int, input().split(",")))
# 1,0,0,0,0,1,0,0,1,0,1
print(nums)
def result(nums):
    n = len(nums)
    leftFree = [0] * n # 表示第i个车位左边空闲车位的个数。
    for i in range(n):
        if nums[i] == 1:
            continue
        # 到这里就是 nums[i] == 0
        if nums[i-1] == 0:
            leftFree[i] = leftFree[i-1] + 1
        else:
            # nums[i-1] == 1
            leftFree[i] = 0 # 时刻想想leftFree的定义是啥。
    # 右边来一遍
    rightFree = [0] * n
    for i in range(n-2, -1, -1): # 注意哟，这里是n-2 最右边的n-1没有意义啊。
        if nums[i] == 1:
            continue
        if nums[i+1] == 0:
            rightFree[i] = rightFree[i+1]+1
        else:
            rightFree[i] = 0
    # 处理边界条件。
    # 如果第0个车位是空闲车位，那么第0个车位的最大距离就是它右边的空闲车位个数
    # 如果第n-1个车位是空闲车位，那么第n-1个车位的最大安全距离就是它左边的空闲车位个数
    ans = max(rightFree[0], leftFree[n-1])

    # 对于第i个车位（i取值1~n-2），其最大距离取min(leftFree[i], rightFree[i])
    for i in range(1, n-1):
        if nums[i]==1:
            continue
        ans = max(ans, min(leftFree[i], rightFree[i]))
    # ans记录的空闲车位数，转化为距离要+1
    return ans+1
print(result(nums))
