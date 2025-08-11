# 给你一个整数 n ，求恰由 n 个节点组成且节点值从 1 到 n 互不相同的 二叉搜索树 有多少种？返回满足题意的二叉搜索树的种数。 
# 
#  
# 
#  示例 1： 
#  
#  
# 输入：n = 3
# 输出：5
#  
# 
#  示例 2： 
# 
#  
# 输入：n = 1
# 输出：1
#  
# 
#  
# 
#  提示： 
# 
#  
#  1 <= n <= 19 
#  
# 
#  Related Topics 树 二叉搜索树 数学 动态规划 二叉树 👍 2659 👎 0

from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    def numTrees1(self, n: int) -> int:
        dp = [0] * 20
        dp[0] = 1  # 空树也算一个
        dp[1] = 1
        dp[2] = 2
        dp[3] = 5
        # dp[4] = 14
        # dp[5] = 42
        # dp[6] = 132
        #
        if n <= 3:
            return dp[n]
        for i in range(4, n + 1):
            for j in range(1, i + 1):
                dp[i] += dp[j - 1] * dp[i - j]
        return dp[n]

    def numTrees(self, n: int) -> int:
        dp = [0] * (n + 1)
        dp[0] = 1  # Empty tree
        dp[1] = 1  # Single node tree
        # 对于 i 个节点，选择第 j 个节点作为根节点时：
        #
        # 左子树有 j-1 个节点，对应的BST数量为 dp[j-1]。
        #
        # 右子树有 i-j 个节点，对应的BST数量为 dp[i-j]。
        #
        # 因此，以 j 为根节点的BST数量为 dp[j-1] * dp[i-j]。
        #
        # 对所有可能的 j 求和，得到 dp[i]。
        # 每一个都尝试做根，然后计算出其左右子树的数量，再乘起来然后加起来。
        for i in range(2, n + 1):
            for j in range(1, i + 1):
                dp[i] += dp[j - 1] * dp[i - j]

        return dp[n]


# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution.numTrees1(5))
