# 给你一个整数数组 prices ，其中 prices[i] 表示某支股票第 i 天的价格。 
# 
#  在每一天，你可以决定是否购买和/或出售股票。你在任何时候 最多 只能持有 一股 股票。你也可以先购买，然后在 同一天 出售。 
# 
#  返回 你能获得的 最大 利润 。 
# 
#  
# 
#  示例 1： 
# 
#  
# 输入：prices = [7,1,5,3,6,4]
# 输出：7
# 解释：在第 2 天（股票价格 = 1）的时候买入，在第 3 天（股票价格 = 5）的时候卖出, 这笔交易所能获得利润 = 5 - 1 = 4。
# 随后，在第 4 天（股票价格 = 3）的时候买入，在第 5 天（股票价格 = 6）的时候卖出, 这笔交易所能获得利润 = 6 - 3 = 3。
# 最大总利润为 4 + 3 = 7 。 
# 
#  示例 2： 
# 
#  
# 输入：prices = [1,2,3,4,5]
# 输出：4
# 解释：在第 1 天（股票价格 = 1）的时候买入，在第 5 天 （股票价格 = 5）的时候卖出, 这笔交易所能获得利润 = 5 - 1 = 4。
# 最大总利润为 4 。 
# 
#  示例 3： 
# 
#  
# 输入：prices = [7,6,4,3,1]
# 输出：0
# 解释：在这种情况下, 交易无法获得正利润，所以不参与交易可以获得最大利润，最大利润为 0。 
# 
#  
# 
#  提示： 
# 
#  
#  1 <= prices.length <= 3 * 10⁴ 
#  0 <= prices[i] <= 10⁴ 
#  
# 
#  Related Topics 贪心 数组 动态规划 👍 2763 👎 0

from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    def maxProfit_wrong(self, prices: List[int]) -> int:
        # 只能买卖一次的情况
        minPrice = float('inf')
        maxProfit = 0
        for price in prices:
            if price < minPrice:
                minPrice = price
            elif price - minPrice > maxProfit:
                maxProfit = price - minPrice
        return maxProfit

    def maxProfit1(self, prices: List[int]) -> int:
        # 买卖多次的情况,可以买了卖了再买
        # dp = [0 for _ in range(len(prices))]
        # dp[i][j] 表示第i天，持有j股票的最大利润
        dp = [[0 for _ in range(2)] for _ in range(len(prices))]
        dp[0][0] = 0
        dp[0][1] = -prices[0]
        # 从第二天开始遍历每一天的价格
        for i in range(1, len(prices)):
            # 第i天不持有股票的最大利润：
            # 1. 前一天就不持有股票，今天继续不持有（利润不变）
            # 2. 前一天持有股票，今天卖出（利润增加prices[i]）
            dp[i][0] = max(dp[i - 1][0], dp[i - 1][1] + prices[i])

            # 第i天持有股票的最大利润：
            # 1. 前一天就持有股票，今天继续持有（利润不变）
            # 2. 前一天不持有股票，今天买入（利润减少prices[i]）
            dp[i][1] = max(dp[i - 1][1], dp[i - 1][0] - prices[i])
        return dp[-1][0]

    def maxProfit2(self, prices: List[int]) -> int:
        # 买卖多次的情况,可以买了卖了再买
        if not prices:
            return 0

            # 初始化动态规划的状态变量
            # cash_hold 表示当前不持有股票时的最大利润
            # stock_hold 表示当前持有股票时的最大利润
        cash_hold = 0  # 初始时未持有股票，利润为0
        stock_hold = -prices[0]  # 初始时持有股票，利润为-prices[0]

        for price in prices[1:]:
            # 更新当前未持有股票的最大利润：
            # 可以选择继续不持有，或者卖出之前持有的股票
            new_cash_hold = max(cash_hold, stock_hold + price)

            # 更新当前持有股票的最大利润：
            # 可以选择继续持有，或者用之前未持有股票的利润买入当前股票
            new_stock_hold = max(stock_hold, cash_hold - price)

            # 更新状态变量
            cash_hold, stock_hold = new_cash_hold, new_stock_hold

        # 最后返回未持有股票时的最大利润
        return cash_hold

    def maxProfit(self, prices: List[int]) -> int:
        if not prices:
            return 0

        max_profit = 0
        for i in range(1, len(prices)):
            if prices[i] > prices[i - 1]:
                max_profit += prices[i] - prices[i - 1]

        return max_profit

# leetcode submit region end(Prohibit modification and deletion)


if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution.maxProfit([7, 1, 5, 3, 6, 4]))
