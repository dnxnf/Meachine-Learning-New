# 峰值元素是指其值严格大于左右相邻值的元素。 
# 
#  给你一个整数数组 nums，找到峰值元素并返回其索引。数组可能包含多个峰值，在这种情况下，返回 任何一个峰值 所在位置即可。 
# 
#  你可以假设 nums[-1] = nums[n] = -∞ 。 
# 
#  你必须实现时间复杂度为 O(log n) 的算法来解决此问题。 
# 
#  
# 
#  示例 1： 
# 
#  
# 输入：nums = [1,2,3,1]
# 输出：2
# 解释：3 是峰值元素，你的函数应该返回其索引 2。 
# 
#  示例 2： 
# 
#  
# 输入：nums = [1,2,1,3,5,6,4]
# 输出：1 或 5 
# 解释：你的函数可以返回索引 1，其峰值元素为 2；
#      或者返回索引 5， 其峰值元素为 6。
#  
# 
#  
# 
#  提示： 
# 
#  
#  1 <= nums.length <= 1000 
#  -2³¹ <= nums[i] <= 2³¹ - 1 
#  对于所有有效的 i 都有 nums[i] != nums[i + 1] 
#  
# 
#  Related Topics 数组 二分查找 👍 1413 👎 0

from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    def findPeakElement(self, nums: List[int]) -> int:
        left, right = 0, len(nums) - 1  # 初始化左右指针
        while left < right:  # 当左右指针未相遇时继续循环
            mid = (left + right) // 2  # 计算中间索引
            if nums[mid] < nums[mid + 1]:  # 如果中间元素小于右侧元素
                left = mid + 1  # 峰值在右侧，调整左指针
            else:  # 否则，峰值在左侧或中间元素本身就是峰值
                right = mid  # 调整右指针
        return left  # 当左右指针相遇时，即为峰值位置


# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution.findPeakElement([1, 2, 3, 1]))
