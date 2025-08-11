# 你是一个专业的小偷，计划偷窃沿街的房屋。每间房内都藏有一定的现金，影响你偷窃的唯一制约因素就是相邻的房屋装有相互连通的防盗系统，如果两间相邻的房屋在同一晚上
# 被小偷闯入，系统会自动报警。 
# 
#  给定一个代表每个房屋存放金额的非负整数数组，计算你 不触动警报装置的情况下 ，一夜之内能够偷窃到的最高金额。 
# 
#  
# 
#  示例 1： 
# 
#  
# 输入：[1,2,3,1]
# 输出：4
# 解释：偷窃 1 号房屋 (金额 = 1) ，然后偷窃 3 号房屋 (金额 = 3)。
#      偷窃到的最高金额 = 1 + 3 = 4 。 
# 
#  示例 2： 
# 
#  
# 输入：[2,7,9,3,1]
# 输出：12
# 解释：偷窃 1 号房屋 (金额 = 2), 偷窃 3 号房屋 (金额 = 9)，接着偷窃 5 号房屋 (金额 = 1)。
#      偷窃到的最高金额 = 2 + 9 + 1 = 12 。
#  
# 
#  
# 
#  提示： 
# 
#  
#  1 <= nums.length <= 100 
#  0 <= nums[i] <= 400 
#  
# 
#  Related Topics 数组 动态规划 👍 3306 👎 0
from functools import lru_cache
from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    def rob1(self, nums: List[int]) -> int:
        # dfs,返回的是偷窃到的最高金额，参数是当前的房子编号
        @lru_cache(None)
        def dfs(i: int):
            # 因为是往后考虑的，所以结束条件式是i>=len(nums)
            if i >= len(nums):
                return 0
            # 偷了当前房子，就不能偷下一个房子
            rob_i = nums[i] + dfs(i + 2)
            # 不偷当前房子，就可以偷下一个房子
            not_rob_i = dfs(i + 1)
            return max(rob_i, not_rob_i)

        return dfs(0)

    def rob(self, nums: List[int]) -> int:
        if len(nums) <= 1:
            return max(nums)
        # 动态规划
        # dp[i]表示偷窃到第i个房子的最大金额
        dp = [0] * len(nums)
        dp[0] = nums[0]
        dp[1] = max(nums[0], nums[1])
        for i in range(2, len(nums)):
            # 选或者不选第i个房子，取最大值
            dp[i] = max(dp[i - 1], dp[i - 2] + nums[i])
        return dp[-1]


# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution.rob([2, 7, 9, 3, 1]))
