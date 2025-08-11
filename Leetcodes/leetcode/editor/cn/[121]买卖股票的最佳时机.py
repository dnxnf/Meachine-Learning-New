# 给定一个数组 prices ，它的第 i 个元素 prices[i] 表示一支给定股票第 i 天的价格。 
# 
#  你只能选择 某一天 买入这只股票，并选择在 未来的某一个不同的日子 卖出该股票。设计一个算法来计算你所能获取的最大利润。 
# 
#  返回你可以从这笔交易中获取的最大利润。如果你不能获取任何利润，返回 0 。 
# 
#  
# 
#  示例 1： 
# 
#  
# 输入：[7,1,5,3,6,4]
# 输出：5
# 解释：在第 2 天（股票价格 = 1）的时候买入，在第 5 天（股票价格 = 6）的时候卖出，最大利润 = 6-1 = 5 。
#      注意利润不能是 7-1 = 6, 因为卖出价格需要大于买入价格；同时，你不能在买入前卖出股票。
#  
# 
#  示例 2： 
# 
#  
# 输入：prices = [7,6,4,3,1]
# 输出：0
# 解释：在这种情况下, 没有交易完成, 所以最大利润为 0。
#  
# 
#  
# 
#  提示： 
# 
#  
#  1 <= prices.length <= 10⁵ 
#  0 <= prices[i] <= 10⁴ 
#  
# 
#  Related Topics 数组 动态规划 👍 3812 👎 0

from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    def maxProfit1(self, prices: List[int]) -> int:
        # 普通循环法,会超时
        maxn = 0
        for i in range(len(prices)):
            for j in range(i + 1, len(prices)):
                if prices[j] > prices[i]:
                    maxn = max(maxn, prices[j] - prices[i])
        return maxn

    def maxProfit2(self, prices: List[int]) -> int:
        # 动态规划,不一定有动态规划表，主要是思想，一步一步的影响后面
        maxPro = 0  # 当前最大利润
        minPrice = prices[0]  # 当前最低价格
        for price in prices:
            if price <= minPrice:
                minPrice = price
            #     当前价格比之前的价格高，计算利润
            else:
                maxPro = max(maxPro, price - minPrice)
        return maxPro

    def maxProfit(self, prices: List[int]) -> int:
        # 手写版
        # 记录最小的，与后面大的比较，记录结果，同时更换小的
        minPrice = prices[0]
        res = 0
        for i, price in enumerate(prices):
            if price > minPrice:
                res = max(price - minPrice, res)
            elif price <= minPrice:
                minPrice = price
        return res


# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution)
