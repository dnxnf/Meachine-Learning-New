# 给你一个整数 n ，返回 和为 n 的完全平方数的最少数量 。 
# 
#  完全平方数 是一个整数，其值等于另一个整数的平方；换句话说，其值等于一个整数自乘的积。例如，1、4、9 和 16 都是完全平方数，而 3 和 11 不是。
#  
# 
#  
# 
#  示例 1： 
# 
#  
# 输入：n = 12
# 输出：3 
# 解释：12 = 4 + 4 + 4 
# 
#  示例 2： 
# 
#  
# 输入：n = 13
# 输出：2
# 解释：13 = 4 + 9 
# 
#  
# 
#  提示： 
# 
#  
#  1 <= n <= 10⁴ 
#  
# 
#  Related Topics 广度优先搜索 数学 动态规划 👍 2201 👎 0

from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    def numSquares(self, n: int) -> int:
        nums = [i * i for i in range(1, int(n ** 0.5) + 1)]
        print(nums)
        dp = [float('inf')] * (n + 1)
        dp[0] = 0
        '''nums里面是1,4,9,16等等
        对于每个元素，都从nums里面走一遍，从最小的开始找，
        '''
        for i in range(1, n + 1):
            for num in nums:
                # 都是从1开始的，如果当前的平方和已经大于i，就超了，可以进行下一个数字了
                # 如果没有超，比如刚好相等，4和4的情况，会变成1，因为4-4=0，再加一。
                if num > i:
                    break
                dp[i] = min(dp[i], dp[i - num] + 1)
        return dp[n]


# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution.numSquares(13))
