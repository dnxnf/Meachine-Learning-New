# 数组的每个下标作为一个阶梯，第 i 个阶梯对应着一个非负数的体力花费值 cost[i]（下标从 0 开始）。 
# 
#  每当爬上一个阶梯都要花费对应的体力值，一旦支付了相应的体力值，就可以选择向上爬一个阶梯或者爬两个阶梯。 
# 
#  请找出达到楼层顶部的最低花费。在开始时，你可以选择从下标为 0 或 1 的元素作为初始阶梯。 
# 
#  
# 
#  示例 1： 
# 
#  
# 输入：cost = [10, 15, 20]
# 输出：15
# 解释：最低花费是从 cost[1] 开始，然后走两步即可到阶梯顶，一共花费 15 。
#  
# 
#  示例 2： 
# 
#  
# 输入：cost = [1, 100, 1, 1, 1, 100, 1, 1, 100, 1]
# 输出：6
# 解释：最低花费方式是从 cost[0] 开始，逐个经过那些 1 ，跳过 cost[3] ，一共花费 6 。
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
#  
# 
#  
#  注意：本题与主站 746 题相同： https://leetcode-cn.com/problems/min-cost-climbing-stairs/ 
# 
# 
#  Related Topics 数组 动态规划 👍 109 👎 0

from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    def minCostClimbingStairs1(self, cost: List[int]) -> int:
        n = len(cost)
        # 这个dp是从当前阶梯网上爬的最小花费，所以要到顶层，取出两个阶梯的最小值
        dp = [0] * n
        dp[0] = cost[0]
        dp[1] = cost[1]
        for i in range(2, n):
            dp[i] = min(dp[i - 1], dp[i - 2]) + cost[i]
        return min(dp[-1], dp[-2])

    def minCostClimbingStairs(self, cost: List[int]) -> int:
        n = len(cost) + 1
        # 这个dp是到达当前阶梯的最小花费
        dp = [0] * n
        dp[0] = 0
        dp[1] = 0
        for i in range(2, n):
            # 要到达这个，得先到前面的，再加上从前往上走的费用
            dp[i] = min(dp[i - 1] + cost[i - 1], dp[i - 2] + cost[i - 2])
            # print(dp)
        return dp[-1]


# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution.minCostClimbingStairs([10, 15, 20]))
