# 给你一个整数数组 nums ，找到其中最长严格递增子序列的长度。 
# 
#  子序列 是由数组派生而来的序列，删除（或不删除）数组中的元素而不改变其余元素的顺序。例如，[3,6,2,7] 是数组 [0,3,1,6,2,2,7] 的子
# 序列。 
# 
#  示例 1： 
# 
#  
# 输入：nums = [10,9,2,5,3,7,101,18]
# 输出：4
# 解释：最长递增子序列是 [2,3,7,101]，因此长度为 4 。
#  
# 
#  示例 2： 
# 
#  
# 输入：nums = [0,1,0,3,2,3]
# 输出：4
#  
# 
#  示例 3： 
# 
#  
# 输入：nums = [7,7,7,7,7,7,7]
# 输出：1
#  
# 
#  
# 
#  提示： 
# 
#  
#  1 <= nums.length <= 2500 
#  -10⁴ <= nums[i] <= 10⁴ 
#  
# 
#  
# 
#  进阶： 
# 
#  
#  你能将算法的时间复杂度降低到 O(n log(n)) 吗? 
#  
# 
#  Related Topics 数组 二分查找 动态规划 👍 4002 👎 0

from typing import List, Optional


# favour 二分加贪心找最长递增子序列，动态规划
# leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    def lengthOfLIS(self, nums: List[int]) -> int:
        tails = []
        for num in nums:
            # 二分查找第一个 >= num 的位置
            left, right = 0, len(tails)
            while left < right:
                mid = (left + right) // 2
                if tails[mid] < num:
                    left = mid + 1
                else:
                    right = mid
            if left == len(tails):
                tails.append(num)
            else:
                tails[left] = num
        print(tails)
        return len(tails)

    def lengthOfLIS2(self, nums: List[int]) -> int:
        # 动态规划
        if not nums:
            return 0
        # dp[i]：表示以nums[i]结尾的最长递增子序列的长度。
        dp = [1] * len(nums)
        for i in range(len(nums)):
            for j in range(i):
                if nums[j] < nums[i]:
                    # dp[i]是会更新的，因此得一直保持一个最大值
                    dp[i] = max(dp[i], dp[j] + 1)
        return max(dp)


# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution.lengthOfLIS([10, 9, 2, 5, 3, 7, 101, 18]))
