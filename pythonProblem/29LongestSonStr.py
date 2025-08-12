#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project  ：MachineLearning 
@File     ：29LongestSonStr.py
@Describe ：PyCharm 
@Author   ：Hello World
@Date     ：2025/5/28 上午10:38
题目： 有 N 个正整数组成的一个序列，给定一个整数 sum，求长度最长的的连续子序列使他们的和等于 sum，
返回次子序列的长度，如果没有满足要求的序列 返回 -1。
2. 输入描述
两行输入，第一行为拼接的正整数序列，第二行为一个整数 sum。
3. 输出描述
满足条件的子序列的长度，如果没有满足要求的序列 返回 -1。
eg:
1,2,3,4,2
6
out:3
'''


def find_longest_subarray(arr, target_sum):
    left = 0
    current_sum = 0
    max_length = -1

    for right in range(len(arr)):
        current_sum += arr[right]

        while current_sum > target_sum and left <= right:
            current_sum -= arr[left]
            left += 1

        if current_sum == target_sum:
            if right - left + 1 > max_length:
                max_length = right - left + 1

    return max_length


# 读取输入
arr = list(map(int, input().split(',')))
target_sum = int(input())

# 调用函数并输出结果
result = find_longest_subarray(arr, target_sum)
print(result)