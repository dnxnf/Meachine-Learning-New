# 小力将 N 个零件的报价存于数组 `nums`。小力预算为 `target`，假定小力仅购买两个零件，要求购买零件的花费不超过预算，请问他有多少种采购方案。
# 
# 
# 注意：答案需要以 `1e9 + 7 (1000000007)` 为底取模，如：计算初始结果为：`1000000008`，请返回 `1`
# 
# **示例 1：**
# 
# > 输入：`nums = [2,5,3,5], target = 6`
# >
# > 输出：`1`
# >
# > 解释：预算内仅能购买 nums[0] 与 nums[2]。
# 
# **示例 2：**
# 
# > 输入：`nums = [2,2,1,9], target = 10`
# >
# > 输出：`4`
# >
# > 解释：符合预算的采购方案如下：
# > nums[0] + nums[1] = 4
# > nums[0] + nums[2] = 3
# > nums[1] + nums[2] = 3
# > nums[2] + nums[3] = 10
# 
# **提示：**
# - `2 <= nums.length <= 10^5`
# - `1 <= nums[i], target <= 10^5`
# 
#  Related Topics 数组 双指针 二分查找 排序 👍 67 👎 0
from functools import lru_cache, cache
from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    # @cache
    def purchasePlans(self, nums: List[int], target: int) -> int:
        nums.sort()
        left, right = 0, len(nums) - 1
        res = 0
        mod = 10 ** 9 + 7

        while left < right:
            if nums[left] + nums[right] <= target:
                res += right - left
                left += 1
            else:
                right -= 1
            # res %= mod  # 防止溢出

        return res % mod


# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution.purchasePlans(nums=[2, 5, 3, 5], target=6))
