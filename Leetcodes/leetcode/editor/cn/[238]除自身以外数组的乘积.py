# 给你一个整数数组 nums，返回 数组 answer ，其中 answer[i] 等于 nums 中除 nums[i] 之外其余各元素的乘积 。 
# 
#  题目数据 保证 数组 nums之中任意元素的全部前缀元素和后缀的乘积都在 32 位 整数范围内。 
# 
#  请 不要使用除法，且在 O(n) 时间复杂度内完成此题。 
# 
#  
# 
#  示例 1: 
# 
#  
# 输入: nums = [1,2,3,4]
# 输出: [24,12,8,6]
#  
# 
#  示例 2: 
# 
#  
# 输入: nums = [-1,1,0,-3,3]
# 输出: [0,0,9,0,0]
#  
# 
#  
# 
#  提示： 
# 
#  
#  2 <= nums.length <= 10⁵ 
#  -30 <= nums[i] <= 30 
#  输入 保证 数组 answer[i] 在 32 位 整数范围内 
#  
# 
#  
# 
#  进阶：你可以在 O(1) 的额外空间复杂度内完成这个题目吗？（ 出于对空间复杂度分析的目的，输出数组 不被视为 额外空间。） 
# 
#  Related Topics 数组 前缀和 👍 2064 👎 0

from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        st = set()
        mul = 1
        for i in range(len(nums)):
            if nums[i] == 0:
                st.add(i)
            else:
                mul = mul * nums[i]
        res = [0] * len(nums)
        if len(st) > 1:
            return res
        # if not st:
        #     return res
        print(mul)
        # 只有一个0的情况
        if len(st) == 1:
            res[st.pop()] = mul
            return res
        for i in range(len(nums)):
            res[i] = mul // nums[i]
        return res


# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution.productExceptSelf([1, 2, 0, 3, 4]))
