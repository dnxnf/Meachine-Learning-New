# 给定一个整数数组
#  prices，其中第 prices[i] 表示第 i 天的股票价格 。 
# 
#  设计一个算法计算出最大利润。在满足以下约束条件下，你可以尽可能地完成更多的交易（多次买卖一支股票）: 
# 
#  
#  卖出股票后，你无法在第二天买入股票 (即冷冻期为 1 天)。 
#  
# 
#  注意：你不能同时参与多笔交易（你必须在再次购买前出售掉之前的股票）。 
# 
#  
# 
#  示例 1: 
# 
#  
# 输入: prices = [1,2,3,0,2]
# 输出: 3 
# 解释: 对应的交易状态为: [买入, 卖出, 冷冻期, 买入, 卖出] 
# 
#  示例 2: 
# 
#  
# 输入: prices = [1]
# 输出: 0
#  
# 
#  
# 
#  提示： 
# 
#  
#  1 <= prices.length <= 5000 
#  0 <= prices[i] <= 1000 
#  
# 
#  Related Topics 数组 动态规划 👍 1863 👎 0
from functools import lru_cache
from typing import List, Optional

# why 完全没看懂的dp
# leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    '''
参数：当前天数index，是否持有股票has_stock，是否处于冷冻期cooldown。
终止条件：当index超过价格序列长度时，返回0。
冷冻期处理：如果处于冷冻期，只能跳过当前天，进入下一天。
不操作：计算不进行任何操作的利润。
持有股票：可以选择卖出股票，进入冷冻期，并计算利润。
不持有股票：可以选择买入股票，并计算利润。
结果返回：从第0天开始，初始状态为不持有股票且不处于冷冻期，调用DFS函数。
    '''
    def maxProfit(self, prices: List[int]) -> int:
        if not prices or len(prices) < 2:
            return 0

        @lru_cache(maxsize=None)
        def dfs(index, has_stock, cooldown):
            if index >= len(prices):
                return 0

            # 如果处于冷冻期，只能跳过
            if cooldown:
                return dfs(index + 1, has_stock, False)

            # 不操作，直接进入下一天
            do_nothing = dfs(index + 1, has_stock, cooldown)

            if has_stock:
                # 卖出股票，进入冷冻期
                sell = dfs(index + 1, False, True) + prices[index]
                return max(do_nothing, sell)
            else:
                # 买入股票
                buy = dfs(index + 1, True, cooldown) - prices[index]
                return max(do_nothing, buy)

        return dfs(0, False, False)

    def maxProfit1(self, prices: List[int]) -> int:
        if not prices or len(prices) < 2:
            return 0

        n = len(prices)
        # 初始化三个状态数组
        hold = [0] * n  # 持有股票时的最大利润
        sold = [0] * n  # 卖出股票时的最大利润
        cooldown = [0] * n  # 冷冻期时的最大利润

        hold[0] = -prices[0]  # 第一天买入股票，利润为负的股票价格

        for i in range(1, n):
            # 持有股票的状态：前一天已经持有，或者前一天是冷冻期今天买入
            hold[i] = max(hold[i - 1], cooldown[i - 1] - prices[i])
            # 卖出股票的状态：只能是前一天持有股票今天卖出
            sold[i] = hold[i - 1] + prices[i]
            # 冷冻期的状态：前一天是冷冻期或者前一天卖出股票
            cooldown[i] = max(cooldown[i - 1], sold[i - 1])

        # 最大利润是最后一天卖出或冷冻期的最大值
        return max(sold[-1], cooldown[-1])


# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution.maxProfit([1, 2, 3, 0, 2]))
