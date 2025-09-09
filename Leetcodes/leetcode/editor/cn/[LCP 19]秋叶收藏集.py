# 小扣出去秋游，途中收集了一些红叶和黄叶，他利用这些叶子初步整理了一份秋叶收藏集 `leaves`， 字符串 `leaves` 仅包含小写字符 `r` 和 `
# y`， 其中字符 `r` 表示一片红叶，字符 `y` 表示一片黄叶。
# 出于美观整齐的考虑，小扣想要将收藏集中树叶的排列调整成「红、黄、红」三部分。每部分树叶数量可以不相等，但均需大于等于 1。每次调整操作，小扣可以将一片红叶替
# 换成黄叶或者将一片黄叶替换成红叶。请问小扣最少需要多少次调整操作才能将秋叶收藏集调整完毕。
# 
# **示例 1：**
# 
# > 输入：`leaves = "rrryyyrryyyrr"`
# >
# > 输出：`2`
# >
# > 解释：调整两次，将中间的两片红叶替换成黄叶，得到 "rrryyyyyyyyrr"
# 
# **示例 2：**
# 
# > 输入：`leaves = "ryr"`
# >
# > 输出：`0`
# >
# > 解释：已符合要求，不需要额外操作
# 
# **提示：**
# - `3 <= leaves.length <= 10^5`
# - `leaves` 中只包含字符 `'r'` 和字符 `'y'`
# 
#  Related Topics 字符串 动态规划 👍 242 👎 0

from typing import List, Optional

'''
动态规划（DP）设置：使用动态数组 dp[i][j]，其中 i 表示当前字符的索引（0到n-1），j 表示当前部分（0,1,2分别代表第一部分、第二部分、第三部分）。

状态转移：

第一部分（j=0）：只能由第一部分转移而来，需要当前字符是 'r'，否则需要一次操作。

第二部分（j=1）：可以从第一部分或第二部分转移而来，需要当前字符是 'y'，否则需要一次操作。

第三部分（j=2）：可以从第二部分或第三部分转移而来，需要当前字符是 'r'，否则需要一次操作。

初始化：dp[0][0] 取决于第一个字符是否为 'r'（如果是，操作0次；否则1次）。其他部分初始化为极大值（因为不可能从第一部分直接跳到第三部分等）。

结果：最终结果是 dp[n-1][2]，表示处理完所有字符且处于第三部分的最小操作次数。
'''


# leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    def minimumOperations(self, leaves: str) -> int:
        dp = [[float('inf')] * 3 for _ in range(len(leaves))]
        dp[0][0] = 0 if leaves[0] == 'r' else 1
        for i in range(1, len(leaves)):
            ch = leaves[i]
            # i是第一部分，
            dp[i][0] = dp[i - 1][0] + (0 if ch == 'r' else 1)
            dp[i][1] = min(dp[i - 1][0], dp[i - 1][1]) + (0 if ch == 'y' else 1)
            dp[i][2] = min(dp[i - 1][1], dp[i - 1][2]) + (0 if ch == 'r' else 1)

        return dp[-1][2]


# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution)
