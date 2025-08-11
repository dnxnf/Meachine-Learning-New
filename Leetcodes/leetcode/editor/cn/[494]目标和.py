# 给你一个非负整数数组 nums 和一个整数 target 。 
# 
#  向数组中的每个整数前添加 '+' 或 '-' ，然后串联起所有整数，可以构造一个 表达式 ： 
# 
#  
#  例如，nums = [2, 1] ，可以在 2 之前添加 '+' ，在 1 之前添加 '-' ，然后串联起来得到表达式 "+2-1" 。 
#  
# 
#  返回可以通过上述方法构造的、运算结果等于 target 的不同 表达式 的数目。 
# 
#  
# 
#  示例 1： 
# 
#  
# 输入：nums = [1,1,1,1,1], target = 3
# 输出：5
# 解释：一共有 5 种方法让最终目标和为 3 。
# -1 + 1 + 1 + 1 + 1 = 3
# +1 - 1 + 1 + 1 + 1 = 3
# +1 + 1 - 1 + 1 + 1 = 3
# +1 + 1 + 1 - 1 + 1 = 3
# +1 + 1 + 1 + 1 - 1 = 3
#  
# 
#  示例 2： 
# 
#  
# 输入：nums = [1], target = 1
# 输出：1
#  
# 
#  
# 
#  提示： 
# 
#  
#  1 <= nums.length <= 20 
#  0 <= nums[i] <= 1000 
#  0 <= sum(nums[i]) <= 1000 
#  -1000 <= target <= 1000 
#  
# 
#  Related Topics 数组 动态规划 回溯 👍 2177 👎 0
from functools import lru_cache
from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    def findTargetSumWays1(self, nums: List[int], target: int) -> int:
        # 回溯法，每个位置都有加减两种选择，所以一共有2^n种可能
        # @lru_cache(None)
        def backtrack(start, cur_sum):
            if start == len(nums):
                if cur_sum == target:
                    self.ans += 1
                return
            backtrack(start + 1, cur_sum + nums[start])
            backtrack(start + 1, cur_sum - nums[start])

        self.ans = 0
        backtrack(0, 0)
        return self.ans

    def findTargetSumWays(self, nums: List[int], target: int) -> int:
        # 回溯法，每个位置都有加减两种选择，所以一共有2^n种可能
        # @lru_cache(None)
        @lru_cache(maxsize=None)
        def backtrack(index, current_sum):
            if index == len(nums):
                return 1 if current_sum == target else 0
            # 当前数字选择加或减
            return backtrack(index + 1, current_sum + nums[index]) + \
                backtrack(index + 1, current_sum - nums[index])

        return backtrack(0, 0)

# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution)
