# 在一个由 '0' 和 '1' 组成的二维矩阵内，找到只包含 '1' 的最大正方形，并返回其面积。 
# 
#  
# 
#  示例 1： 
#  
#  
# 输入：matrix = [["1","0","1","0","0"],["1","0","1","1","1"],["1","1","1","1","1"]
# ,["1","0","0","1","0"]]
# 输出：4
#  
# 
#  示例 2： 
#  
#  
# 输入：matrix = [["0","1"],["1","0"]]
# 输出：1
#  
# 
#  示例 3： 
# 
#  
# 输入：matrix = [["0"]]
# 输出：0
#  
# 
#  
# 
#  提示： 
# 
#  
#  m == matrix.length 
#  n == matrix[i].length 
#  1 <= m, n <= 300 
#  matrix[i][j] 为 '0' 或 '1' 
#  
# 
#  Related Topics 数组 动态规划 矩阵 👍 1813 👎 0

from typing import List, Optional


# 从1往后面弄，左，上，左上都是1，则右下角为2，这样就是边长
class Solution:
    def maximalSquare(self, matrix: List[List[str]]) -> int:
        m, n = len(matrix), len(matrix[0])
        dp = [[0] * n for _ in range(m)]
        res = 0
        for i in range(m):
            for j in range(n):
                if matrix[i][j] == '1':
                    if i == 0 or j == 0:
                        dp[i][j] = 1
                    else:
                        dp[i][j] = min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1]) + 1
                    res = max(res, dp[i][j])
        return res * res



# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution.maximalSquare([["1","0","1","0","0"],["1","0","1","1","1"],["1","1","1","1","1"],["1","0","0","1","0"]]))
