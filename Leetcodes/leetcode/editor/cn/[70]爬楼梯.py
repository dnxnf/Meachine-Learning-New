# 假设你正在爬楼梯。需要 n 阶你才能到达楼顶。 
# 
#  每次你可以爬 1 或 2 个台阶。你有多少种不同的方法可以爬到楼顶呢？ 
# 
#  
# 
#  示例 1： 
# 
#  
# 输入：n = 2
# 输出：2
# 解释：有两种方法可以爬到楼顶。
# 1. 1 阶 + 1 阶
# 2. 2 阶 
# 
#  示例 2： 
# 
#  
# 输入：n = 3
# 输出：3
# 解释：有三种方法可以爬到楼顶。
# 1. 1 阶 + 1 阶 + 1 阶
# 2. 1 阶 + 2 阶
# 3. 2 阶 + 1 阶
#  
# 
#  
# 
#  提示： 
# 
#  
#  1 <= n <= 45 
#  
# 
#  Related Topics 记忆化搜索 数学 动态规划 👍 3833 👎 0
from functools import cache, lru_cache
from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    def climbStairs1(self, n: int) -> int:
        # 动态规划,每个台阶可以有前两个到达的方式和再相加
        # dp[i] = dp[i-1] + dp[i-2]
        # dp存放的是到此路径有几种方法
        if n == 1:
            return 1
        if n == 2:
            return 2
        dp = [0] * (n + 1)
        dp[1] = 1
        dp[2] = 2
        for i in range(3, n + 1):
            dp[i] = dp[i - 1] + dp[i - 2]
        return dp[n]

    def climbStairs2(self, n: int) -> int:
        # 普通回溯法，会超时，下面是改进的
        if n == 1:
            return 1
        if n == 2:
            return 2

        # 回溯法,考虑当前状态,，当前每一步的选择，
        # 当前状态的目标（或者总目标）以及最后的结果
        # 当前state，target，结果数量
        # res = 0
        def backtrack(choices, state, target):
            nonlocal res
            if state == target:
                res += 1
            for i in choices:
                if state + i > n:
                    continue
                backtrack(choices, state + i, target)

        choices = [1, 2]
        state = 0
        res = 0
        # 每次能上1或2个台阶，当前位于0，目标是到达n
        backtrack(choices, state, n)
        return res

    def climbStairs3(self, n: int) -> int:

        # 升级的回溯,因为目标不变，每一步的选择不变，因此只传递当前的状态
        # note cache 不能使用列表，参数必须是可哈希的（如整数、字符串、元组等），而列表是不可哈希的。
        #  并且必须使用return,不能全局变量,因为其是根据返回值来缓存的
        @cache
        def backtrack(state):
            # nonlocal choices, res
            if state == n:  # 当前到了目标点
                return 1
            if state > n:
                return 0  # 超过阶数，没有路径
            res1 = backtrack(state + 1)
            res2 = backtrack(state + 2)
            return res1 + res2

        res = backtrack(0)
        return res

    def climbStairs4(self, n: int) -> int:
        #         第二遍手写版
        if n <= 2:
            return n
        dp = [0 for _ in range(n + 1)]
        dp[1] = 1
        dp[2] = 2
        for i in range(3, n + 1):
            dp[i] = dp[i - 1] + dp[i - 2]
        return dp[n]

    def climbStairs(self, n: int) -> int:
        #         手写板只用两个数字
        if n <= 2:
            return n
        a = 1
        b = 2
        c = 0
        for i in range(3, n + 1):
            c = a + b
            a = b
            b = c
        return c


# leetcode submit region end(Prohibit modification and deletion)


if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution.climbStairs(2))
