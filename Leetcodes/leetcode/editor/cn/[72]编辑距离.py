# 给你两个单词 word1 和 word2， 请返回将 word1 转换成 word2 所使用的最少操作数 。 
# 
#  你可以对一个单词进行如下三种操作： 
# 
#  
#  插入一个字符 
#  删除一个字符 
#  替换一个字符 
#  
# 
#  
# 
#  示例 1： 
# 
#  
# 输入：word1 = "horse", word2 = "ros"
# 输出：3
# 解释：
# horse -> rorse (将 'h' 替换为 'r')
# rorse -> rose (删除 'r')
# rose -> ros (删除 'e')
#  
# 
#  示例 2： 
# 
#  
# 输入：word1 = "intention", word2 = "execution"
# 输出：5
# 解释：
# intention -> inention (删除 't')
# inention -> enention (将 'i' 替换为 'e')
# enention -> exention (将 'n' 替换为 'x')
# exention -> exection (将 'n' 替换为 'c')
# exection -> execution (插入 'u')
#  
# 
#  
# 
#  提示： 
# 
#  
#  0 <= word1.length, word2.length <= 500 
#  word1 和 word2 由小写英文字母组成 
#  
# 
#  Related Topics 字符串 动态规划 👍 3700 👎 0
from functools import cache, lru_cache
from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
# favour 编辑距离，动态规划，记忆化搜索，dfs
class Solution:
    def minDistance1(self, word1: str, word2: str) -> int:
        # dfs 可能过不了
        # 果然，超时了
        if word1 == word2:
            return 0
        m, n = len(word1), len(word2)
        if m == 0:
            return n
        if n == 0:
            return m
        if word1[m - 1] == word2[n - 1]:
            return self.minDistance(word1[:m - 1], word2[:n - 1])
        else:
            return 1 + min(self.minDistance(word1[:m - 1], word2[:n]),
                           self.minDistance(word1, word2[:n - 1]),
                           self.minDistance(word1[:m - 1], word2[:n - 1]))

    def minDistance2(self, word1: str, word2: str) -> int:
        # 记忆化搜索,不用管是怎么做的，只要知道返回的是最小编辑距离就行
        # 写出返回条件，自动就对了。
        m, n = len(word1), len(word2)

        # 记忆化搜索,需要传递的对象必须是可哈希的(也就是不可变的）：
        # 这是因为缓存需要将参数作为字典的键来存储和查找结果，
        # 而字典的键必须是不可变的（如整数、字符串、元组等）
        @lru_cache(maxsize=None)
        def dfs(i: int, j: int) -> int:
            # 若 word1 为空，则需要插入 j+1 个字符（word2 剩下的全部字符）。
            if i == -1:
                return j + 1
            # 若 word2 为空，则需要删除 i+1 个字符（word1 剩下的全部字符）。
            if j == -1:
                return i + 1
            # 如果两个字符相同，则不需要操作，从前一位操作
            if word1[i] == word2[j]:
                return dfs(i - 1, j - 1)
            # 若不同，对应了三种情况，分别是删除，插入，替换
            # i-1,j对应删除当前字符，让word1从前一个字符开始与这个匹配，i,j-1对应插入，i-1,j-1对应替换，
            # 因为i-1是word1从前一个字符开始，就是吧word1的最后一个字符删掉，所以i-1对应删除
            # 取三者中最小值
            else:
                return 1 + min(dfs(i - 1, j), dfs(i, j - 1), dfs(i - 1, j - 1))

        return dfs(m - 1, n - 1)

    def minDistance(self, word1: str, word2: str) -> int:
        # 动态规划
        m, n = len(word1), len(word2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        # 初始化,当word1为空时，dp[i][0] = i,当word2为空时，dp[0][j] = j
        for i in range(m + 1):
            dp[i][0] = i
        for j in range(n + 1):
            dp[0][j] = j
        # 状态转移方程，当word1[i-1] == word2[j-1]时,当前字符不用处理，dp[i][j] = dp[i-1][j-1]
        # 否则，dp[i][j] = 1 + min(dp[i-1][j],dp[i][j-1],dp[i-1][j-1])
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if word1[i - 1] == word2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1]
                else:
                    dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])
        return dp[m][n]


# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution.minDistance2("horse", "ros"))
