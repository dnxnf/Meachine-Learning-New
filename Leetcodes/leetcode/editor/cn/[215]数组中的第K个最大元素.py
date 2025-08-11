# 给定整数数组 nums 和整数 k，请返回数组中第 k 个最大的元素。 
# 
#  请注意，你需要找的是数组排序后的第 k 个最大的元素，而不是第 k 个不同的元素。 
# 
#  你必须设计并实现时间复杂度为 O(n) 的算法解决此问题。 
# 
#  
# 
#  示例 1: 
# 
#  
# 输入: [3,2,1,5,6,4], k = 2
# 输出: 5
#  
# 
#  示例 2: 
# 
#  
# 输入: [3,2,3,1,2,4,5,5,6], k = 4
# 输出: 4 
# 
#  
# 
#  提示： 
# 
#  
#  1 <= k <= nums.length <= 10⁵ 
#  -10⁴ <= nums[i] <= 10⁴ 
#  
# 
#  Related Topics 数组 分治 快速选择 排序 堆（优先队列） 👍 2755 👎 0

from typing import List, Optional

# leetcode submit region begin(Prohibit modification and deletion)
# favour 堆，找第k大/小，O(n)
import heapq


class Solution:
    def findKthLargest1(self, nums: List[int], k: int) -> int:
        # o(nlog n)
        nums.sort()
        return nums[-k]

    def findKthLargest(self, nums: List[int], k: int) -> int:
        # o(nlog(n))
        heap = []
        for num in nums:
            if len(heap) < k:
                heapq.heappush(heap, num)
            else:
                if num > heap[0]:
                    heapq.heappop(heap)
                    heapq.heappush(heap, num)
        return heap[0]


# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution.findKthLargest([3, 2, 1, 5, 6, 4], 2))
