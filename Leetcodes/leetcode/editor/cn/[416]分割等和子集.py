# 给你一个 只包含正整数 的 非空 数组 nums 。请你判断是否可以将这个数组分割成两个子集，使得两个子集的元素和相等。 
# 
#  
# 
#  示例 1： 
# 
#  
# 输入：nums = [1,5,11,5]
# 输出：true
# 解释：数组可以分割成 [1, 5, 5] 和 [11] 。 
# 
#  示例 2： 
# 
#  
# 输入：nums = [1,2,3,5]
# 输出：false
# 解释：数组不能分割成两个元素和相等的子集。
#  
# 
#  
# 
#  提示： 
# 
#  
#  1 <= nums.length <= 200 
#  1 <= nums[i] <= 100 
#  
# 
#  Related Topics 数组 动态规划 👍 2355 👎 0

from typing import List, Optional
# favour 动态规划思想，子集合加反向遍历
# leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    def canPartition(self, nums: List[int]) -> bool:
        sumn = sum(nums)
        # nums.sort()
        # 是奇数肯定不能返回
        if sumn % 2 != 0:
            return False
        # 如果是偶数，那么就是一半,能组成一半，那就可以
        sumn = sumn // 2
        n = len(nums)
        # dp存储的是能不能达到某个数值，dp[i]表示能不能达到i
        dp = [False] * (sumn + 1)
        # 初始全false，0可以达到（不选就可以）
        dp[0] = True
        # 遍历nums，每个数字都可以选或者不选，
        # 选了就是dp[i-nums[i]]，不选就是dp[i]
        for i in range(n):
            # 倒着遍历，从目标到当前所选数字i,防止倍数或重复
            for j in range(sumn, nums[i] - 1, -1):
                dp[j] = dp[j] or dp[j - nums[i]]
        return dp[sumn]
# dp[j] = dp[j] or dp[j - num] 表示：
# 如果之前已经可以组成和为 j 的子集（dp[j] 为 True），那么保持 True；
# 否则，检查是否可以通过加上当前的 num 来组成和为 j 的子集（即 dp[j - num] 是否为 True）。
#j 从 11 到 5：
# j = 11: dp[11] = dp[11] or dp[6]（dp[6] 为 False，dp[11] 保持 False）。
# j = 10: dp[10] = dp[10] or dp[5]（dp[5] 为 False，dp[10] 保持 False）。
# j = 6: dp[6] = dp[6] or dp[1]（dp[1] 为 True，所以 dp[6] 变为 True）。
# j = 5: dp[5] = dp[5] or dp[0]（dp[0] 为 True，所以 dp[5] 变为 True）。

# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution.canPartition([1, 5, 11, 5]))