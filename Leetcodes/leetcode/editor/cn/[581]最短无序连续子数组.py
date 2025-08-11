# 给你一个整数数组 nums ，你需要找出一个 连续子数组 ，如果对这个子数组进行升序排序，那么整个数组都会变为升序排序。 
# 
#  请你找出符合题意的 最短 子数组，并输出它的长度。 
# 
#  
# 
#  
#  
#  示例 1： 
#  
#  
# 
#  
# 输入：nums = [2,6,4,8,10,9,15]
# 输出：5
# 解释：你只需要对 [6, 4, 8, 10, 9] 进行升序排序，那么整个表都会变为升序排序。
#  
# 
#  示例 2： 
# 
#  
# 输入：nums = [1,2,3,4]
# 输出：0
#  
# 
#  示例 3： 
# 
#  
# 输入：nums = [1]
# 输出：0
#  
# 
#  
# 
#  提示： 
# 
#  
#  1 <= nums.length <= 10⁴ 
#  -10⁵ <= nums[i] <= 10⁵ 
#  
# 
#  
# 
#  进阶：你可以设计一个时间复杂度为 O(n) 的解决方案吗？ 
# 
#  Related Topics 栈 贪心 数组 双指针 排序 单调栈 👍 1217 👎 0

from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
# favour 滑动窗口，双指针的好题
class Solution:
    def findUnsortedSubarray(self, nums: List[int]) -> int:
        # 找到一个子数组，使得这个数组之前的元素都小于等于这个子数组，之后的元素都大于等于这个子数组。
        # 这个子数组就是我们要找的最短无序连续子数组。
        # 用window记录当前的无序数组，用left和right记录当前的无序数组的左右边界。
        n = len(nums)
        # 处理特殊情况：数组为空或只有一个元素，本身就是有序的
        if n <= 1:
            return 0

        # 第一步：从左向右找第一个不满足升序的位置
        left = 0
        while left < n - 1 and nums[left] <= nums[left + 1]:
            left += 1
        # 如果已经遍历到末尾，说明整个数组是有序的
        if left == n - 1:
            return 0

        # 第二步：从右向左找第一个不满足升序的位置
        right = n - 1
        while right > 0 and nums[right] >= nums[right - 1]:
            right -= 1

        # 第三步：在初步确定的[left, right]窗口内找最小值和最大值
        window_min = min(nums[left:right + 1])
        window_max = max(nums[left:right + 1])

        # 第四步：向左扩展左边界，找到第一个小于等于window_min的位置
        while left > 0 and nums[left - 1] > window_min:
            left -= 1

        # 第五步：向右扩展右边界，找到第一个大于等于window_max的位置
        while right < n - 1 and nums[right + 1] < window_max:
            right += 1

        # 返回需要排序的子数组长度
        return right - left + 1



# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution)
