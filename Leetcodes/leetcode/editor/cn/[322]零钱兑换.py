# 给你一个整数数组 coins ，表示不同面额的硬币；以及一个整数 amount ，表示总金额。 
# 
#  计算并返回可以凑成总金额所需的 最少的硬币个数 。如果没有任何一种硬币组合能组成总金额，返回 -1 。 
# 
#  你可以认为每种硬币的数量是无限的。 
# 
#  
# 
#  示例 1： 
# 
#  
# 输入：coins = [1, 2, 5], amount = 11
# 输出：3 
# 解释：11 = 5 + 5 + 1 
# 
#  示例 2： 
# 
#  
# 输入：coins = [2], amount = 3
# 输出：-1 
# 
#  示例 3： 
# 
#  
# 输入：coins = [1], amount = 0
# 输出：0
#  
# 
#  
# 
#  提示： 
# 
#  
#  1 <= coins.length <= 12 
#  1 <= coins[i] <= 2³¹ - 1 
#  0 <= amount <= 10⁴ 
#  
# 
#  Related Topics 广度优先搜索 数组 动态规划 👍 3092 👎 0
from collections import deque
from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    def coinChange1(self, coins: List[int], amount: int) -> int:
        dp = [float('inf')] * (amount + 1)
        dp[0] = 0
        for i in range(1, amount + 1):
            for coin in coins:
                # note 和[279]的dp思路差不多，当前的数量就是可用的钱数那个加一
                if i >= coin:
                    dp[i] = min(dp[i], dp[i - coin] + 1)
        return dp[amount] if dp[amount] != float('inf') else -1

    def coinChange2(self, coins: List[int], amount: int) -> int:
        # 当成逐层扩展，知道找到目标金额，因为把已经有的金额加到了visited，又是逐层的，所有是找到最小的数量
        # 使用队列来进行BFS，队列中的元素是（当前金额，硬币数）
        q = deque([(0, 0)])
        # 使用集合来记录已经访问过的金额，避免重复处理
        visited = set()
        while q:
            money, num = q.popleft()
            # 如果当前金额等于目标金额，返回当前硬币数
            if money == amount:
                return num
            # 如果当前金额超过目标金额，跳过
            if money > amount:
                continue
            # 遍历所有硬币，生成新的金额
            for coin in coins:
                new_amount = money + coin
                if new_amount not in visited:
                    visited.add(new_amount)
                    q.append((new_amount, num + 1))
        # 如果队列为空仍未找到解，返回-1
        return -1

    def coinChange(self, coins: List[int], amount: int) -> int:
        # dp 完全背包，每个物品都能拿任意次，所以dp[i]表示凑够i元钱需要的最少硬币数
        dp = [float('inf')] * (amount + 1)
        dp[0] = 0
        # 先初始化dp[0]，因为0元钱可以凑成0个硬币
        for i in range(1, amount + 1):
            for coin in coins: # 这里就无需倒序，因为这是完全背包，所以顺序无所谓
                if i >= coin:
                    dp[i] = min(dp[i], dp[i - coin] + 1)
        return dp[amount] if dp[amount] != float('inf') else -1
# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution.coinChange([1, 2, 5], 11))
