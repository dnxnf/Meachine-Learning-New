# 给定一个不含重复数字的数组 nums ，返回其 所有可能的全排列 。你可以 按任意顺序 返回答案。 
# 
#  
# 
#  示例 1： 
# 
#  
# 输入：nums = [1,2,3]
# 输出：[[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]
#  
# 
#  示例 2： 
# 
#  
# 输入：nums = [0,1]
# 输出：[[0,1],[1,0]]
#  
# 
#  示例 3： 
# 
#  
# 输入：nums = [1]
# 输出：[[1]]
#  
# 
#  
# 
#  提示： 
# 
#  
#  1 <= nums.length <= 6 
#  -10 <= nums[i] <= 10 
#  nums 中的所有整数 互不相同 
#  
# 
#  Related Topics 数组 回溯 👍 3114 👎 0

from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    def permute1(self, nums: List[int]) -> List[List[int]]:
        # 回溯法
        res = []
        path = []

        # 回溯
        def backtrack(num):
            # 返回条件，达到条件了再加
            if len(path) == len(num):
                res.append(path[:])
                return

            for i in range(len(num)):
                # 当前数字没被加进去
                if nums[i] not in path:
                    path.append(num[i])
                    backtrack(num)
                    path.pop()

        backtrack(nums)
        return res

    def permute2(self, nums: List[int]) -> List[List[int]]:
        # dfs,其实和回溯基本一样
        res = []

        # 使用dfs，remain是剩下可选的，path是当前已选择的路径
        def dfs(remain, path):
            if not remain:
                res.append(path[:])
                return
            # 遍历remain，每次加入path
            for i in range(len(remain)):
                path.append(remain[i])
                dfs(remain[:i] + remain[i + 1:], path)
                path.pop()

        dfs(nums, [])
        return res

    def permute(self, nums: List[int]) -> List[List[int]]:
        # 回溯法
        res = []
        # path = []

        # 回溯
        def backtrack(num, path):
            if len(path) == len(num):
                res.append(path[:])
                return

            for i in range(len(num)):
                # 当前数字没被加进去
                if nums[i] not in path:
                    path.append(num[i])
                    backtrack(num, path)
                    path.pop()

        backtrack(nums, [])
        return res




# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution.permute(nums=[1, 2, 3]))
