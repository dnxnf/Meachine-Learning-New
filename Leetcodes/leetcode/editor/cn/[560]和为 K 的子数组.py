# 给你一个整数数组 nums 和一个整数 k ，请你统计并返回 该数组中和为 k 的子数组的个数 。 
# 
#  子数组是数组中元素的连续非空序列。 
# 
#  
# 
#  示例 1： 
# 
#  
# 输入：nums = [1,1,1], k = 2
# 输出：2
#  
# 
#  示例 2： 
# 
#  
# 输入：nums = [1,2,3], k = 3
# 输出：2
#  
# 
#  
# 
#  提示： 
# 
#  
#  1 <= nums.length <= 2 * 10⁴ 
#  -1000 <= nums[i] <= 1000 
#  -10⁷ <= k <= 10⁷ 
#  
# 
#  Related Topics 数组 哈希表 前缀和 👍 2820 👎 0
from collections import defaultdict
from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
# favour 前缀和
class Solution:
    def subarraySum_wrong(self, nums: List[int], k: int) -> int:
        # 没考虑负数，并且window没啥用
        if len(nums) == 1:
            return 1 if nums[0] == k else 0
        window_sum = 0
        window = []
        left = 0
        count = 0
        for right, num in enumerate(nums):
            window_sum += num
            while window_sum > k:
                window_sum -= window[left]
                left += 1
            if window_sum == k:
                count += 1
            window.append(num)
        return count

    def subarraySum(self, nums: List[int], k: int) -> int:
        prefix_sum = defaultdict(int)
        prefix_sum[0] = 1  # 初始前缀和为0出现1次
        current_sum = 0
        count = 0

        for num in nums:
            current_sum += num
            # 查找是否有prefix_sum[j] - k = prefix_sum[i]
            count += prefix_sum.get(current_sum - k, 0)
            # 更新当前前缀和的出现次数
            prefix_sum[current_sum] += 1

        return count


# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution)
