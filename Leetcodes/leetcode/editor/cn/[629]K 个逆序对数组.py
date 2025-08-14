# 对于一个整数数组 nums，逆序对是一对满足 0 <= i < j < nums.length 且 nums[i] > nums[j]的整数对 [i, j]
#  。 
# 
#  给你两个整数 n 和 k，找出所有包含从 1 到 n 的数字，且恰好拥有 k 个 逆序对 的不同的数组的个数。由于答案可能很大，只需要返回对 10⁹ + 
# 7 取余的结果。 
# 
#  
# 
#  示例 1： 
# 
#  
# 输入：n = 3, k = 0
# 输出：1
# 解释：
# 只有数组 [1,2,3] 包含了从1到3的整数并且正好拥有 0 个逆序对。
#  
# 
#  示例 2： 
# 
#  
# 输入：n = 3, k = 1
# 输出：2
# 解释：
# 数组 [1,3,2] 和 [2,1,3] 都有 1 个逆序对。
#  
# 
#  
# 
#  提示： 
# 
#  
#  1 <= n <= 1000 
#  0 <= k <= 1000 
#  
# 
#  Related Topics 动态规划 👍 325 👎 0

from typing import List, Optional

# leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    def kInversePairs(self, n: int, k: int) -> int:
        
# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution)