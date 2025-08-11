# 给你一个整数数组 cost ，其中 cost[i] 是从楼梯第 i 个台阶向上爬需要支付的费用。一旦你支付此费用，即可选择向上爬一个或者两个台阶。 
# 
#  你可以选择从下标为 0 或下标为 1 的台阶开始爬楼梯。 
# 
#  请你计算并返回达到楼梯顶部的最低花费。 
# 
#  
# 
#  示例 1： 
# 
#  
# 输入：cost = [10,15,20]
# 输出：15
# 解释：你将从下标为 1 的台阶开始。
# - 支付 15 ，向上爬两个台阶，到达楼梯顶部。
# 总花费为 15 。
#  
# 
#  示例 2： 
# 
#  
# 输入：cost = [1,100,1,1,1,100,1,1,100,1]
# 输出：6
# 解释：你将从下标为 0 的台阶开始。
# - 支付 1 ，向上爬两个台阶，到达下标为 2 的台阶。
# - 支付 1 ，向上爬两个台阶，到达下标为 4 的台阶。
# - 支付 1 ，向上爬两个台阶，到达下标为 6 的台阶。
# - 支付 1 ，向上爬一个台阶，到达下标为 7 的台阶。
# - 支付 1 ，向上爬两个台阶，到达下标为 9 的台阶。
# - 支付 1 ，向上爬一个台阶，到达楼梯顶部。
# 总花费为 6 。
#  
# 
#  
# 
#  提示： 
# 
#  
#  2 <= cost.length <= 1000 
#  0 <= cost[i] <= 999 
#  
# 
#  Related Topics 数组 动态规划 👍 1667 👎 0

from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    def minCostClimbingStairs1(self, cost: List[int]) -> int:
        n = len(cost)
        dp0 = [0] * (n + 2)
        dp1 = [0] * (n + 2)
        # dp[i]记录爬到第i个台阶的最小花费
        # dp[i] = min(dp[i - 1], dp[i - 2])
        # 两次dp，一次从0开始，一次从1开始
        dp0[0] = 0
        dp0[1] = cost[0]
        for i in range(2, n + 1):
            dp0[i] = min(dp0[i - 1] + cost[i - 1], dp0[i - 2] + cost[i - 2])

        dp1[1] = 0
        dp1[2] = cost[1]
        for i in range(3, n + 1):
            dp1[i] = min(dp1[i - 1] + cost[i - 1], dp1[i - 2] + cost[i - 2])
        return min(dp0[n], dp1[n])
    def minCostClimbingStairs(self, cost: List[int]) -> int:
        # dp表示从第i阶出发的最小花费
        n = len(cost)
        dp = [0] * n
        dp[0] = cost[0]
        dp[1] = cost[1]
        for i in range(2, n):
            dp[i] = cost[i] + min(dp[i - 1], dp[i - 2])
        return min(dp[n - 1], dp[n - 2])

# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution.minCostClimbingStairs([10, 15, 20]))
