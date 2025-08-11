# 给你一个整数数组 nums 。如果任一值在数组中出现 至少两次 ，返回 true ；如果数组中每个元素互不相同，返回 false 。
# 
#  
# 
#  示例 1： 
# 
#  
#  输入：nums = [1,2,3,1] 
#  
# 
#  输出：true 
# 
#  解释： 
# 
#  元素 1 在下标 0 和 3 出现。 
# 
#  示例 2： 
# 
#  
#  输入：nums = [1,2,3,4] 
#  
# 
#  输出：false 
# 
#  解释： 
# 
#  所有元素都不同。 
# 
#  示例 3： 
# 
#  
#  输入：nums = [1,1,1,3,3,4,3,2,4,2] 
#  
# 
#  输出：true 
# 
#  
# 
#  提示： 
# 
#  
#  1 <= nums.length <= 10⁵ 
#  -10⁹ <= nums[i] <= 10⁹ 
#  
# 
#  Related Topics 数组 哈希表 排序 👍 1135 👎 0

from typing import List, Optional

# leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:
        dic = {}
        for num in nums:
            if num in dic: # in dic，访问的是key
                return True
            else:
                dic[num] = 1
        return False
# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution)