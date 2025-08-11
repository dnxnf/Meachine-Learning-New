# 给你一个按照非递减顺序排列的整数数组 nums，和一个目标值 target。请你找出给定目标值在数组中的开始位置和结束位置。 
# 
#  如果数组中不存在目标值 target，返回 [-1, -1]。 
# 
#  你必须设计并实现时间复杂度为 O(log n) 的算法解决此问题。 
# 
#  
# 
#  示例 1： 
# 
#  
# 输入：nums = [5,7,7,8,8,10], target = 8
# 输出：[3,4] 
# 
#  示例 2： 
# 
#  
# 输入：nums = [5,7,7,8,8,10], target = 6
# 输出：[-1,-1] 
# 
#  示例 3： 
# 
#  
# 输入：nums = [], target = 0
# 输出：[-1,-1] 
# 
#  
# 
#  提示： 
# 
#  
#  0 <= nums.length <= 10⁵ 
#  -10⁹ <= nums[i] <= 10⁹ 
#  nums 是一个非递减数组 
#  -10⁹ <= target <= 10⁹ 
#  
# 
#  Related Topics 数组 二分查找 👍 3041 👎 0

from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    def searchRange1(self, nums: List[int], target: int) -> List[int]:
        # ologn ,，遍历不行，二分查找
        res = [-1, -1]
        left, right = 0, len(nums) - 1
        while left <= right:
            mid = (left + right) // 2
            if nums[mid] == target:
                res[0] = mid
                res[1] = mid
                # 找到中间值后向左右找第一个和最后一个
                while res[0] - 1 >= 0 and nums[res[0] - 1] == target:
                    res[0] -= 1
                while res[1] + 1 <= len(nums) - 1 and nums[res[1] + 1] == target:
                    res[1] += 1
                return res
            # 没找到target，判断target在左边还是右边
            elif nums[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        return res

    def searchRange(self, nums: List[int], target: int) -> List[int]:
        # o(n)的写法
        res = [-1, -1]
        for i in range(len(nums)):
            if nums[i] == target:
                res[0] = i
                break
        if res[0] == -1:
            return res
        # 先从前往后，找到第一个，再从后往前，找到最后一个
        for i in range(len(nums) - 1, -1, -1):
            if nums[i] == target:
                res[1] = i
                break
        return res


# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution.searchRange([5, 7, 7, 8, 8, 10], 8))
