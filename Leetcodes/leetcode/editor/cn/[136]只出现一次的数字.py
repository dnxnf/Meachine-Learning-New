# 给你一个 非空 整数数组 nums ，除了某个元素只出现一次以外，其余每个元素均出现两次。找出那个只出现了一次的元素。 
# 
#  你必须设计并实现线性时间复杂度的算法来解决此问题，且该算法只使用常量额外空间。 
# 
#  
#  
#  
#  
#  
# 
#  示例 1 ： 
# 
#  
#  输入：nums = [2,2,1] 
#  
# 
#  输出：1 
# 
#  示例 2 ： 
# 
#  
#  输入：nums = [4,1,2,1,2] 
#  
# 
#  输出：4 
# 
#  示例 3 ： 
# 
#  
#  输入：nums = [1] 
#  
# 
#  输出：1 
# 
#  
# 
#  提示： 
# 
#  
#  1 <= nums.length <= 3 * 10⁴ 
#  -3 * 10⁴ <= nums[i] <= 3 * 10⁴ 
#  除了某个元素只出现一次以外，其余每个元素均出现两次。 
#  
# 
#  Related Topics 位运算 数组 👍 3338 👎 0

from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    def singleNumber1(self, nums: List[int]) -> int:
        # 手写版
        dic = {}
        for i, num in enumerate(nums):
            # favour 存储字典值，有则加1，无则1
            dic[num] = dic.get(num, 0) + 1
        # print(dic)
        # note 遍历字典用items()
        for k, v in dic.items():
            # print(k, v)
            if v == 1:
                return k
    def singleNumber(self, nums: List[int]) -> int:
        # 位运算版
        res = 0
        for num in nums:
            res ^= num
        return res

# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution.singleNumber([4, 1, 2, 1, 2]))
