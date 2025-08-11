# 给定一个 m x n 的整数数组 grid。一个机器人初始位于 左上角（即 grid[0][0]）。机器人尝试移动到 右下角（即 grid[m - 1][
# n - 1]）。机器人每次只能向下或者向右移动一步。 
# 
#  网格中的障碍物和空位置分别用 1 和 0 来表示。机器人的移动路径中不能包含 任何 有障碍物的方格。 
# 
#  返回机器人能够到达右下角的不同路径数量。 
# 
#  测试用例保证答案小于等于 2 * 10⁹。 
# 
#  
# 
#  示例 1： 
#  
#  
# 输入：obstacleGrid = [[0,0,0],[0,1,0],[0,0,0]]
# 输出：2
# 解释：3x3 网格的正中间有一个障碍物。
# 从左上角到右下角一共有 2 条不同的路径：
# 1. 向右 -> 向右 -> 向下 -> 向下
# 2. 向下 -> 向下 -> 向右 -> 向右
#  
# 
#  示例 2： 
#  
#  
# 输入：obstacleGrid = [[0,1],[0,0]]
# 输出：1
#  
# 
#  
# 
#  提示： 
# 
#  
#  m == obstacleGrid.length 
#  n == obstacleGrid[i].length 
#  1 <= m, n <= 100 
#  obstacleGrid[i][j] 为 0 或 1 
#  
# 
#  Related Topics 数组 动态规划 矩阵 👍 1423 👎 0

from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    def uniquePathsWithObstacles1(self, Grid: List[List[int]]) -> int:
        m = len(Grid)
        if m == 0:
            return 0
        n = len(Grid[0])
        if n == 0:
            return 0

        # 如果起点或终点是障碍物，直接返回0
        if Grid[0][0] == 1 or Grid[m - 1][n - 1] == 1:
            return 0

        dp = [[0 for _ in range(n)] for _ in range(m)]
        dp[0][0] = 1

        # 初始化第一列
        for i in range(1, m):
            # 如果是障碍物
            if Grid[i][0] == 1:
                dp[i][0] = 0
            else:
                dp[i][0] = dp[i - 1][0]

        # 初始化第一行
        for j in range(1, n):
            if Grid[0][j] == 1:
                dp[0][j] = 0
            else:
                dp[0][j] = dp[0][j - 1]

        for i in range(1, m):
            for j in range(1, n):
                if Grid[i][j] == 1:
                    dp[i][j] = 0
                else:
                    dp[i][j] = dp[i - 1][j] + dp[i][j - 1]

        return dp[m - 1][n - 1]

    def uniquePathsWithObstacles(self, grid: List[List[int]]) -> int:
        # 自己写一遍
#          如果起点或终点是障碍物，直接返回0，否则初始化dp
        if grid[0][0] == 1 or grid[-1][-1] == 1:
            return 0
        # 初始化
        dp = [[0] * len(grid[0]) for _ in range(len(grid))]
        dp[0][0] = 1
        # 第一列初始化，
        for i in range(1, len(grid)):
            if 1 == grid[i][0]:
                dp[i][0] = 0
            else:
                dp[i][0] = dp[i - 1][0]
#         第一行初始化
        for i in range(1, len(grid[0])):
            if 1 == grid[0][i]:
                dp[0][i] = 0
            else:
                dp[0][i] = dp[0][i - 1]
#         初始化完了，直接dp
        for i in range(1, len(grid)):
            for j in range(1, len(grid[0])):
                if 1 == grid[i][j]:
                    dp[i][j] = 0
                else:
                    dp[i][j] = dp[i - 1][j] + dp[i][j - 1]
        return dp[-1][-1]


# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution.uniquePathsWithObstacles([[0, 0, 0], [0, 1, 0], [0, 0, 0]]))
