# 给你一个整数数组 nums ，数组中的元素 互不相同 。返回该数组所有可能的子集（幂集）。 
# 
#  解集 不能 包含重复的子集。你可以按 任意顺序 返回解集。 
# 
#  
# 
#  示例 1： 
# 
#  
# 输入：nums = [1,2,3]
# 输出：[[],[1],[2],[1,2],[3],[1,3],[2,3],[1,2,3]]
#  
# 
#  示例 2： 
# 
#  
# 输入：nums = [0]
# 输出：[[],[0]]
#  
# 
#  
# 
#  提示： 
# 
#  
#  1 <= nums.length <= 10 
#  -10 <= nums[i] <= 10 
#  nums 中的所有元素 互不相同 
#  
# 
#  Related Topics 位运算 数组 回溯 👍 2501 👎 0

from typing import List, Optional


# what 回溯法基础
# leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    def subsets1(self, nums: List[int]) -> List[List[int]]:
        res = []
        path = []

        def bactrack(nums, idx):
            # 开局先加，大于了才返回
            res.append(path[:])
            if idx >= len(nums):
                return
            for i in range(idx, len(nums)):
                path.append(nums[i])
                bactrack(nums, i + 1)
                path.pop()

        bactrack(nums, 0)
        return res

    # dfs试一下
    def subsets2(self, nums: List[int]) -> List[List[int]]:
        res = []

        def dfs(start, path):
            # 先添加
            res.append(path.copy())

            for i in range(start, len(nums)):
                path.append(nums[i])
                dfs(i + 1, path)
                path.pop()

        dfs(0, [])
        return res

    def subsets(self, nums: List[int]) -> List[List[int]]:
        res = []

        def dfs(start, path):
            res.append(path)
            for i in range(start, len(nums)):
                # start就是i+1，从i后面的那个位置开始遍历,但是不能直接i+1，
                # 所以得有个变量来记录一下i+1
                # i + 1确保不会重复使用同一个元素
                dfs(i + 1, path + [nums[i]])

        dfs(0, [])
        return res


# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution.subsets([1, 2, 3]))
