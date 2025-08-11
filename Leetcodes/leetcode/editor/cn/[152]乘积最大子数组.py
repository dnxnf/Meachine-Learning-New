# 给你一个整数数组 nums ，请你找出数组中乘积最大的非空连续 子数组（该子数组中至少包含一个数字），并返回该子数组所对应的乘积。 
# 
#  测试用例的答案是一个 32-位 整数。 
# 
#  
# 
#  示例 1: 
# 
#  
# 输入: nums = [2,3,-2,4]
# 输出: 6
# 解释: 子数组 [2,3] 有最大乘积 6。
#  
# 
#  示例 2: 
# 
#  
# 输入: nums = [-2,0,-1]
# 输出: 0
# 解释: 结果不能为 2, 因为 [-2,-1] 不是子数组。 
# 
#  
# 
#  提示: 
# 
#  
#  1 <= nums.length <= 2 * 10⁴ 
#  -10 <= nums[i] <= 10 
#  nums 的任何子数组的乘积都 保证 是一个 32-位 整数 
#  
# 
#  Related Topics 数组 动态规划 👍 2457 👎 0

from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    def maxProduct(self, nums: List[int]) -> int:
        if not nums:
            return 0
        maxn, minn, res = nums[0], nums[0], nums[0]
        # 有负数，则最大乘积可能为负数，最小乘积可能为正数
        for i in range(1, len(nums)):
            if nums[i] < 0:
                maxn, minn = minn, maxn
            # 遇到一个就更新，所以不用拆开考虑后面的数组
            maxn = max(nums[i], maxn * nums[i])
            minn = min(nums[i], minn * nums[i])
            res = max(res, maxn)
        return res


# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution.maxProduct([2, 3, -2, 4]))
