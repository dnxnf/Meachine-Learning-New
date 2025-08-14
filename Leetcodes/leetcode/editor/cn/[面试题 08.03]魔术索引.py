# 魔术索引。 在数组A[0...n-1]中，有所谓的魔术索引，满足条件A[i] = i。给定一个有序整数数组，编写一种方法找出魔术索引，若有的话，在数组A中找
# 出一个魔术索引，如果没有，则返回-1。若有多个魔术索引，返回索引值最小的一个。 
# 
#  示例 1： 
# 
#  
#  输入：nums = [0, 2, 3, 4, 5]
#  输出：0
#  说明：0下标的元素为0
#  
# 
#  示例 2： 
# 
#  
#  输入：nums = [1, 1, 1]
#  输出：1
#  
# 
#  说明： 
# 
#  
#  nums长度在[1, 1000000]之间 
#  此题为原书中的 Follow-up，即数组中可能包含重复元素的版本 
#  
# 
#  Related Topics 数组 二分查找 👍 136 👎 0

from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    def findMagicIndex1(self, nums: List[int]) -> int:
        for i, num in enumerate(nums):
            if i == num:
                return i
        return -1

    def findMagicIndex_wrong(self, nums: List[int]) -> int:
        # 不适用于【0,0,2】这种情况
        left, right = 0, len(nums) - 1
        while left <= right:
            mid = (left + right) // 2
            if nums[mid] == mid:
                return mid
            elif nums[mid] > mid:
                right = mid - 1
            elif nums[mid] <= mid:
                left = mid + 1
        return -1

# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution)
