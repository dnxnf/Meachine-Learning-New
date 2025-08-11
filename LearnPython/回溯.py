#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project     ：MachineLearning 
@File        ：回溯.py
@Description ：
@Author      ：Hello World
@Date        ：2025/6/7 上午9:45 
'''
from typing import List

'''
通用模板
res = []    # 存放所欲符合条件结果的集合
path = []   # 存放当前符合条件的结果
def backtracking(nums):             # nums 为选择元素列表
    if 遇到边界条件:                  # 说明找到了一组符合条件的结果
        res.append(path[:])         # 将当前符合条件的结果放入集合中
        return

    for i in range(len(nums)):      # 枚举可选元素列表
        path.append(nums[i])        # 选择元素
        backtracking(nums)          # 递归搜索
        path.pop()                  # 撤销选择

backtracking(nums)
'''


class Solution:
    # 全排列,leetcd46
    def permute(self, nums: List[int]) -> List[List[int]]:
        res = []  # 存放所有符合条件结果的集合
        path = []  # 存放当前符合条件的结果

        def backtracking(nums):  # nums 为选择元素列表
            if len(path) == len(nums):  # 说明找到了一组符合条件的结果
                res.append(path[:])  # 将当前符合条件的结果放入集合中
                return

            for i in range(len(nums)):  # 枚举可选元素列表
                if nums[i] not in path:  # 从当前路径中没有出现的数字中选择
                    path.append(nums[i])  # 选择元素
                    backtracking(nums)  # 递归搜索
                    path.pop()  # 撤销选择

        backtracking(nums)
        return res

    # 子集合,leetcd 78
    #  输入：nums = [1,2,3]
    #  输出：[[],[1],[2],[1,2],[3],[1,3],[2,3],[1,2,3]]
    def subsets(self, nums: List[int]) -> List[List[int]]:
        res = []
        path = []

        def backtrack(nums, idx):
            # 将当前符合条件的结果放入集合中
            res.append(path[:])
            # 终止条件，索引等于长度后即越界
            if idx >= len(nums):
                return

            for i in range(idx, len(nums)):
                path.append(nums[i])
                backtrack(nums, i + 1)
                path.pop()

        backtrack(nums, 0)
        return res

    # leetcd39
    # 输入：candidates = [2,3,6,7], target = 7 输出：[[2,2,3],[7]]
    # 解释： 2 和 3 可以形成一组候选，2 + 2 + 3 = 7 。注意 2 可以使用多次。 7 也是一个候选， 7 = 7 。 仅有这两种组合。
    def combinationSum(self, cad: List[int], tar: int) -> List[List[int]]:
        # 当前选择的，剩余的金额，开始的地方
        def backtrack(combination, remaining, start):
            # combination：当前选择的商品组合
            # remaining：还需要凑的金额
            # start：从哪个商品开始尝试（避免重复组合）
            # 如果剩余金额正好为0，说明找到一组解,递归结束条件
            if remaining == 0:
                result.append(list(combination))
                return
            # 从start开始尝试每个商品
            for i in range(start, len(cad)):
                # 如果商品价格超过剩余金额，跳过（剪枝）
                if cad[i] > remaining:
                    # 已经排序，break和Continue都行，没有排序只能continue
                    break
                # 选择这个商品
                combination.append(cad[i])
                # 继续尝试用这个商品凑剩余金额（因为可以重复使用）
                backtrack(combination, remaining - cad[i], i)
                # 撤销选择，尝试其他可能性
                combination.pop()

        #   ---------- 回溯法 ----------
        result = []
        cad.sort()  # 先排序，方便剪枝
        backtrack([], tar, 0)
        return result


if __name__ == '__main__':
    s = Solution()
    print(s.permute([1, 2, 3]))
    print(s.subsets([1, 2, 3]))
    print(s.combinationSum([2, 3, 6, 7], 7))

# 回溯法
# def nested_for_loop(n):
