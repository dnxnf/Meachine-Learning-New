# 给定一个 m x n 整数矩阵 matrix ，找出其中 最长递增路径 的长度。 
# 
#  对于每个单元格，你可以往上，下，左，右四个方向移动。 不能 在 对角线 方向上移动或移动到 边界外（即不允许环绕）。 
# 
#  
# 
#  示例 1： 
# 
#  
# 
#  
# 输入：matrix = [[9,9,4],[6,6,8],[2,1,1]]
# 输出：4 
# 解释：最长递增路径为 [1, 2, 6, 9]。 
# 
#  示例 2： 
# 
#  
# 
#  
# 输入：matrix = [[3,4,5],[3,2,6],[2,2,1]]
# 输出：4 
# 解释：最长递增路径是 [3, 4, 5, 6]。注意不允许在对角线方向上移动。
#  
# 
#  示例 3： 
# 
#  
# 输入：matrix = [[1]]
# 输出：1
#  
# 
#  
# 
#  提示： 
# 
#  
#  m == matrix.length 
#  n == matrix[i].length 
#  1 <= m, n <= 200 
#  0 <= matrix[i][j] <= 2³¹ - 1 
#  
# 
#  
# 
#  
#  注意：本题与主站 329 题相同： https://leetcode-cn.com/problems/longest-increasing-path-
# in-a-matrix/ 
# 
#  Related Topics 深度优先搜索 广度优先搜索 图 拓扑排序 记忆化搜索 数组 动态规划 矩阵 👍 56 👎 0
from functools import lru_cache
from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    def longestIncreasingPath1(self, matrix: List[List[int]]) -> int:

        # 定义res，用于存储最长递增路径的长度，对每个元素都深搜一次
        # why 这个每次只搜了一个方向，不是对四个方向都搜
        res = 0
        m, n = len(matrix), len(matrix[0])
        diection = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # 上下左右

        @lru_cache(None)
        def dfs(i, j):
            nonlocal res
            res = 1
            for di, dj in diection:
                ni, nj = i + di, j + dj
                if 0 <= ni < m and 0 <= nj < n and matrix[ni][nj] > matrix[i][j]:
                    res = max(res, 1 + dfs(ni, nj))
            return res

        # 遍历矩阵，对每个元素深搜
        for i in range(m):
            for j in range(n):
                res = max(res, dfs(i, j))
        return res

    def longestIncreasingPath2(self, matrix: List[List[int]]) -> int:
        if not matrix or not matrix[0]:
            return 0

        m, n = len(matrix), len(matrix[0])
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # 上下左右

        @lru_cache(None)
        def dfs(i, j):
            max_len = 1
            for di, dj in directions:
                ni, nj = i + di, j + dj
                if 0 <= ni < m and 0 <= nj < n and matrix[ni][nj] > matrix[i][j]:
                    max_len = max(max_len, 1 + dfs(ni, nj))
            return max_len

        res = 0
        for i in range(m):
            for j in range(n):
                res = max(res, dfs(i, j))

        return res

    def longestIncreasingPath(self, matrix: List[List[int]]) -> int:
        # 使用广搜，记录每个位置的最长递增路径长度
        m, n = len(matrix), len(matrix[0])
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # 上下左右
        dp = [[0] * n for _ in range(m)]
        res = 0
        # dp[i][j]表示以(i,j)为起点的最长递增路径长度
        def dfs(i, j):
            nonlocal res
            if dp[i][j] > 0:
                return dp[i][j]
            max_len = 1
            for di, dj in directions:
                ni, nj = i + di, j + dj
                if 0 <= ni < m and 0 <= nj < n and matrix[ni][nj] > matrix[i][j]:
                    max_len = max(max_len, 1 + dfs(ni, nj))
            dp[i][j] = max_len
            res = max(res, max_len)
            return max_len

        for i in range(m):
            for j in range(n):
                dfs(i, j)

        return res


# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution.longestIncreasingPath([[3, 4, 5], [3, 2, 6], [2, 2, 1]]))
    print(solution.longestIncreasingPath2([[9, 9, 4], [6, 6, 8], [2, 1, 1]]))
