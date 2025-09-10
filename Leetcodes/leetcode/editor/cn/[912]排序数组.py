# 给你一个整数数组 nums，请你将该数组升序排列。 
# 
#  你必须在 不使用任何内置函数 的情况下解决问题，时间复杂度为 O(nlog(n))，并且空间复杂度尽可能小。 
# 
#  
# 
#  
#  
# 
#  示例 1： 
# 
#  
# 输入：nums = [5,2,3,1]
# 输出：[1,2,3,5]
# 解释：数组排序后，某些数字的位置没有改变（例如，2 和 3），而其他数字的位置发生了改变（例如，1 和 5）。
#  
# 
#  示例 2： 
# 
#  
# 输入：nums = [5,1,1,2,0,0]
# 输出：[0,0,1,1,2,5]
# 解释：请注意，nums 的值不一定唯一。
#  
# 
#  
# 
#  提示： 
# 
#  
#  1 <= nums.length <= 5 * 10⁴ 
#  -5 * 10⁴ <= nums[i] <= 5 * 10⁴ 
#  
# 
#  Related Topics 数组 分治 桶排序 计数排序 基数排序 排序 堆（优先队列） 归并排序 👍 1149 👎 0

from typing import List, Optional


# :: 快速排序
# leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    def quickSort1(self, nums: List[int]):
        # 简单好理解，但是占空间大
        if len(nums) <= 1:
            return nums
        left, right = [], []
        pivot = nums[0]
        for num in nums[1:]:
            if num < pivot:
                left.append(num)
            else:
                right.append(num)
        return self.quickSort1(left) + [pivot] + self.quickSort1(right)

    def quickSort2(self,nums, low=0, high=None):
        if high is None:
            high = len(nums) - 1
        if low < high:
            # 分区操作，返回 pivot 的正确位置
            pivot_idx = self.partition(nums, low, high)
            # 递归排序左半部分（包含 pivot）
            self.quickSort2(nums, low, pivot_idx)
            # 递归排序右半部分（不包含 pivot）
            self.quickSort2(nums, pivot_idx + 1, high)
        return nums

    def partition(self,nums, low, high):
        pivot = nums[low]  # 选择第一个元素作为 pivot
        i = low + 1
        j = high
        while True:
            while i <= j and nums[i] < pivot:
                i += 1
            while i <= j and nums[j] > pivot:
                j -= 1
            if i >= j:
                break
            nums[i], nums[j] = nums[j], nums[i]
            i += 1
            j -= 1
        # 将 pivot 放到正确的位置
        nums[low], nums[j] = nums[j], nums[low]
        return j  # 返回 pivot 的最终位置

    def sortArray(self, nums: List[int]) -> List[int]:
        return self.quickSort2(nums)
# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution.quickSort2([5, 2, 3, 1]))
