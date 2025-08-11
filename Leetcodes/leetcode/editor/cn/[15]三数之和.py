# 给你一个整数数组 nums ，判断是否存在三元组 [nums[i], nums[j], nums[k]] 满足 i != j、i != k 且 j != 
# k ，同时还满足 nums[i] + nums[j] + nums[k] == 0 。请你返回所有和为 0 且不重复的三元组。 
# 
#  注意：答案中不可以包含重复的三元组。 
# 
#  
# 
#  
# 
#  示例 1： 
# 
#  
# 输入：nums = [-1,0,1,2,-1,-4]
# 输出：[[-1,-1,2],[-1,0,1]]
# 解释：
# nums[0] + nums[1] + nums[2] = (-1) + 0 + 1 = 0 。
# nums[1] + nums[2] + nums[4] = 0 + 1 + (-1) = 0 。
# nums[0] + nums[3] + nums[4] = (-1) + 2 + (-1) = 0 。
# 不同的三元组是 [-1,0,1] 和 [-1,-1,2] 。
# 注意，输出的顺序和三元组的顺序并不重要。
#  
# 
#  示例 2： 
# 
#  
# 输入：nums = [0,1,1]
# 输出：[]
# 解释：唯一可能的三元组和不为 0 。
#  
# 
#  示例 3： 
# 
#  
# 输入：nums = [0,0,0]
# 输出：[[0,0,0]]
# 解释：唯一可能的三元组和为 0 。
#  
# 
#  
# 
#  提示： 
# 
#  
#  3 <= nums.length <= 3000 
#  -10⁵ <= nums[i] <= 10⁵ 
#  
# 
#  Related Topics 数组 双指针 排序 👍 7528 👎 0

from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
# favour 双指针好题，有跳过元素的思想
class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        nums.sort()
        result = []
        n = len(nums)
        # 一个循环遍历所有元素，再在里面遍历后面的元素
        # 双指针，一个从前往后，一个从后往前，比较和，大于等于小于0，分别移动指针
        # 移动时候要跳过重复的元素，因为不能有一样的三元组，相当于是两次跳过:循环开始时和得到结果后
        # 得到结果时跳过：因为三元组不能一样，所以得把其余相等的刨去。
        # 开始时跳过：因为一样的元素在内循环已经走过了
        for i in range(n - 2):
            if i > 0 and nums[i] == nums[i - 1]:
                continue  # 跳过重复的元素,因为不包含重复的三元组

            left, right = i + 1, n - 1
            while left < right:
                total = nums[i] + nums[left] + nums[right]
                if total < 0:
                    left += 1
                elif total > 0:
                    right -= 1
                else:
                    result.append([nums[i], nums[left], nums[right]])
                    # 跳过重复的元素
                    while left < right and nums[left] == nums[left + 1]:
                        left += 1
                    while left < right and nums[right] == nums[right - 1]:
                        right -= 1
                    left += 1
                    right -= 1
        return result


# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution)
