# 给定一个包含 [0, n] 中 n 个数的数组 nums ，找出 [0, n] 这个范围内没有出现在数组中的那个数。 
# 
#  
#  
# 
#  
# 
#  示例 1： 
# 
#  
#  输入：nums = [3,0,1] 
#  
# 
#  输出：2 
# 
#  解释：n = 3，因为有 3 个数字，所以所有的数字都在范围 [0,3] 内。2 是丢失的数字，因为它没有出现在 nums 中。 
# 
#  示例 2： 
# 
#  
#  输入：nums = [0,1] 
#  
# 
#  输出：2 
# 
#  解释：n = 2，因为有 2 个数字，所以所有的数字都在范围 [0,2] 内。2 是丢失的数字，因为它没有出现在 nums 中。 
# 
#  示例 3： 
# 
#  
#  输入：nums = [9,6,4,2,3,5,7,0,1] 
#  
# 
#  输出：8 
# 
#  解释：n = 9，因为有 9 个数字，所以所有的数字都在范围 [0,9] 内。8 是丢失的数字，因为它没有出现在 nums 中。 
# 
#  提示： 
# 
#  
#  n == nums.length 
#  1 <= n <= 10⁴ 
#  0 <= nums[i] <= n 
#  nums 中的所有数字都 独一无二 
#  
# 
#  
# 
#  进阶：你能否实现线性时间复杂度、仅使用额外常数空间的算法解决此问题? 
# 
#  Related Topics 位运算 数组 哈希表 数学 二分查找 排序 👍 883 👎 0

from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    def missingNumber1(self, nums: List[int]) -> int:
        n = len(nums)
        nums.sort()
        for i in range(n):
            if nums[i] != i:
                return i
        return n

    def missingNumber(self, nums: List[int]) -> int:
        n = len(nums)
        expected_sum = n * (n + 1) // 2
        actual_sum = sum(nums)
        return expected_sum - actual_sum


# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution.missingNumber([9, 6, 4, 2, 3, 5, 7, 0, 1]))
