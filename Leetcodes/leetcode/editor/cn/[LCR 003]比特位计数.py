# 给定一个非负整数 n ，请计算 0 到 n 之间的每个数字的二进制表示中 1 的个数，并输出一个数组。 
# 
#  
# 
#  示例 1: 
# 
#  
# 输入: n = 2
# 输出: [0,1,1]
# 解释: 
# 0 --> 0
# 1 --> 1
# 2 --> 10
#  
# 
#  示例 2: 
# 
#  
# 输入: n = 5
# 输出: [0,1,1,2,1,2]
# 解释:
# 0 --> 0
# 1 --> 1
# 2 --> 10
# 3 --> 11
# 4 --> 100
# 5 --> 101
#  
# 
#  
# 
#  说明 : 
# 
#  
#  0 <= n <= 10⁵ 
#  
# 
#  
# 
#  进阶: 
# 
#  
#  给出时间复杂度为 O(n*sizeof(integer)) 的解答非常容易。但你可以在线性时间 O(n) 内用一趟扫描做到吗？ 
#  要求算法的空间复杂度为 O(n) 。 
#  你能进一步完善解法吗？要求在C++或任何其他语言中不使用任何内置函数（如 C++ 中的 __builtin_popcount ）来执行此操作。 
#  
# 
#  
# 
#  
#  注意：本题与主站 338 题相同：https://leetcode-cn.com/problems/counting-bits/ 
# 
#  Related Topics 位运算 动态规划 👍 160 👎 0

from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    def countBits(self, n: int) -> List[int]:
        if n == 0:
            return [0]
        if n == 1:
            return [0, 1]
        if n == 2:
            return [0, 1, 1]
        dp = [0] * (n + 1)
        dp[1] = 1
        dp[2] = 1
        # [0, 1, 1]
        # n>2时候，也就是说从第三项开始，
        # 递推公式：当n是2的次方时，dp[n]为1
        # 当n不是2的次方，比如3
        # 0,1,1,2,1,2,2,3,1,2,2,3,2,3,3,4,1,2,2,3,2,3,3,4,2,3,3,4,3,4,4,5,1,2,2,3,2,3,3,4,2,3,3,4,3,4,4,5,2,3,3,4,3,4,4,5,3,4,4,5,4,5,5,6,1,2,2,3,2,3,3,4,2,3,3,4,3,4,4,5,2,3,3,4,3,4,4,5,3,4,4,5,4,5,5,6,2,3,3,4,3,4,4,
        for i in range(3, n + 1):
            if i & 1 == 0:
                dp[i] = dp[i >> 1]
            else:
                dp[i] = dp[i - 1] + 1
        return dp


# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution.countBits(10))
