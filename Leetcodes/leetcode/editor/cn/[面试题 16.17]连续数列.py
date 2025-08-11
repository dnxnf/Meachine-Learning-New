# 给定一个整数数组，找出总和最大的连续数列，并返回总和。 
# 
#  示例： 
# 
#  输入： [-2,1,-3,4,-1,2,1,-5,4]
# 输出： 6
# 解释： 连续子数组 [4,-1,2,1] 的和最大，为 6。
#  
# 
#  进阶： 
# 
#  如果你已经实现复杂度为 O(n) 的解法，尝试使用更为精妙的分治法求解。 
# 
#  Related Topics 数组 分治 动态规划 👍 153 👎 0

from typing import List, Optional

# leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        dp = [0] * len(nums)
        dp[0] = nums[0]
        # 要么从当前开始，要么把这个加入上次的结果
        # 所以dp[i] = max(nums[i], dp[i-1] + nums[i])
        for i in range(1, len(nums)):
            dp[i] = max(nums[i], dp[i-1] + nums[i])
        return max(dp)
# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution)