# 给你一个非负整数数组 nums ，你最初位于数组的 第一个下标 。数组中的每个元素代表你在该位置可以跳跃的最大长度。 
# 
#  判断你是否能够到达最后一个下标，如果可以，返回 true ；否则，返回 false 。 
# 
#  
# 
#  示例 1： 
# 
#  
# 输入：nums = [2,3,1,1,4]
# 输出：true
# 解释：可以先跳 1 步，从下标 0 到达下标 1, 然后再从下标 1 跳 3 步到达最后一个下标。
#  
# 
#  示例 2： 
# 
#  
# 输入：nums = [3,2,1,0,4]
# 输出：false
# 解释：无论怎样，总会到达下标为 3 的位置。但该下标的最大跳跃长度是 0 ， 所以永远不可能到达最后一个下标。
#  
# 
#  
# 
#  提示： 
# 
#  
#  1 <= nums.length <= 10⁴ 
#  0 <= nums[i] <= 10⁵ 
#  
# 
#  Related Topics 贪心 数组 动态规划 👍 3092 👎 0

from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    def canJump1(self, nums: List[int]) -> bool:
        # dp，存两个东西，能否到当前节点，当前节点能否到最后节点,
        # 如果有节点是1,1，说明到最后了
        n = len(nums)
        if n == 1:
            return True

        dp = [False] * n
        dp[0] = True  # 起点可以到达

        for i in range(n):
            if dp[i]:  # 如果当前位置可以到达
                max_jump = nums[i]
                # 从当前位置可以跳跃到 i+1 到 i+max_jump 的位置
                for j in range(1, max_jump + 1):
                    if i + j < n:
                        dp[i + j] = True
                        if i + j == n - 1:  # 如果已经可以到达终点
                            return True
                    else:
                        break  # 超出数组范围，停止跳跃
        return dp[n - 1]
    def canJump(self, nums: List[int]) -> bool:
        # n = len(nums)
        max_reach = 0  # 记录当前能跳到的最远距离
        n = len(nums)
        # 遍历数组，更新能跳到的最远距离
        for i in range(n):
            if i > max_reach:
                return False
            max_reach = max(max_reach, i + nums[i])
            if max_reach >= n - 1:
                return True
        # return True
# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution.canJump([2, 3, 1, 1, 4]))
