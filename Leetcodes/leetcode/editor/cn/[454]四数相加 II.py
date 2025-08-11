# 给你四个整数数组 nums1、nums2、nums3 和 nums4 ，数组长度都是 n ，请你计算有多少个元组 (i, j, k, l) 能满足： 
# 
#  
#  0 <= i, j, k, l < n 
#  nums1[i] + nums2[j] + nums3[k] + nums4[l] == 0 
#  
# 
#  
# 
#  示例 1： 
# 
#  
# 输入：nums1 = [1,2], nums2 = [-2,-1], nums3 = [-1,2], nums4 = [0,2]
# 输出：2
# 解释：
# 两个元组如下：
# 1. (0, 0, 0, 1) -> nums1[0] + nums2[0] + nums3[0] + nums4[1] = 1 + (-2) + (-1)
#  + 2 = 0
# 2. (1, 1, 0, 0) -> nums1[1] + nums2[1] + nums3[0] + nums4[0] = 2 + (-1) + (-1)
#  + 0 = 0
#  
# 
#  示例 2： 
# 
#  
# 输入：nums1 = [0], nums2 = [0], nums3 = [0], nums4 = [0]
# 输出：1
#  
# 
#  
# 
#  提示： 
# 
#  
#  n == nums1.length 
#  n == nums2.length 
#  n == nums3.length 
#  n == nums4.length 
#  1 <= n <= 200 
#  -2²⁸ <= nums1[i], nums2[i], nums3[i], nums4[i] <= 2²⁸ 
#  
# 
#  Related Topics 数组 哈希表 👍 1134 👎 0

from typing import List, Optional

# leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    def fourSumCount(self, nums1: List[int], nums2: List[int], nums3: List[int], nums4: List[int]) -> int:
        dic = {}
        for i in nums1:
            for j in nums2:
                dic[i+j] = dic.get(i+j, 0) + 1
        res = 0
        for i in nums3:
            for j in nums4:
                if -i-j in dic:
                    res += dic[-i-j]
        return res
# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution)