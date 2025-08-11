# 给你一个整数 n ，请你找出并返回第 n 个 丑数 。 
# 
#  丑数 就是质因子只包含 2、3 和 5 的正整数。 
# 
#  
# 
#  示例 1： 
# 
#  
# 输入：n = 10
# 输出：12
# 解释：[1, 2, 3, 4, 5, 6, 8, 9, 10, 12] 是由前 10 个丑数组成的序列。
#  
# 
#  示例 2： 
# 
#  
# 输入：n = 1
# 输出：1
# 解释：1 通常被视为丑数。
#  
# 
#  
# 
#  提示： 
# 
#  
#  1 <= n <= 1690 
#  
# 
#  Related Topics 哈希表 数学 动态规划 堆（优先队列） 👍 1262 👎 0

from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    def nthUglyNumber(self, n: int) -> int:
        dp = [1] * (n + 1)
        p2, p3, p5 = 1, 1, 1
        for i in range(2, n + 1):
            num2 = dp[p2] * 2
            num3 = dp[p3] * 3
            num5 = dp[p5] * 5
            dp[i] = min(num2, num3, num5)
            if dp[i] == num2:
                p2 += 1
            if dp[i] == num3:
                p3 += 1
            if dp[i] == num5:
                p5 += 1

        return dp[-1]
    # leetcode submit region end(Prohibit modification and deletion)


if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution.nthUglyNumber(10))
