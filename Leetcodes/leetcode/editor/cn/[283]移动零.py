# 给定一个数组 nums，编写一个函数将所有 0 移动到数组的末尾，同时保持非零元素的相对顺序。 
# 
#  请注意 ，必须在不复制数组的情况下原地对数组进行操作。 
# 
#  
# 
#  示例 1: 
# 
#  
# 输入: nums = [0,1,0,3,12]
# 输出: [1,3,12,0,0]
#  
# 
#  示例 2: 
# 
#  
# 输入: nums = [0]
# 输出: [0] 
# 
#  
# 
#  提示: 
#  
# 
#  
#  1 <= nums.length <= 10⁴ 
#  -2³¹ <= nums[i] <= 2³¹ - 1 
#  
# 
#  
# 
#  进阶：你能尽量减少完成的操作次数吗？ 
# 
#  Related Topics 数组 双指针 👍 2657 👎 0

from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)

class Solution:
    def moveZeroes1(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        if not nums:
            return
        if len(nums) == 1:
            return
        # 双指针
        i, j = 0, 1
        while j < len(nums):
            if nums[i] == 0 and nums[j] != 0:
                nums[i], nums[j] = nums[j], nums[i]
                i += 1
                j += 1
            elif nums[i] == 0 and nums[j] == 0:
                j += 1
            elif nums[i] != 0 and nums[j] != 0:
                i += 1
                j += 1
            elif nums[i] != 0 and nums[j] == 0:
                i += 1
                j += 1

        # 双指针

    def moveZeroes(self, nums: List[int]) -> None:
        i, j = 0, 0
        for _ in range(len(nums)):
            if nums[i] == 0 and nums[j] != 0:
                nums[i], nums[j] = nums[j], nums[i]
                i += 1
                j += 1
            elif nums[i] == 0 and nums[j] == 0:
                j += 1
            elif nums[i] != 0 and nums[j] != 0:
                i += 1
                j += 1
            elif nums[i] != 0 and nums[j] == 0:
                i += 1
                j += 1

# leetcode submit region end(Prohibit modification and deletion)


if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution)
