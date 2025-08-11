# 给定一个由 0 和 1 组成的非空二维数组 grid ，用来表示海洋岛屿地图。 
# 
#  一个 岛屿 是由一些相邻的 1 (代表土地) 构成的组合，这里的「相邻」要求两个 1 必须在水平或者竖直方向上相邻。你可以假设 grid 的四个边缘都被 
# 0（代表水）包围着。 
# 
#  找到给定的二维数组中最大的岛屿面积。如果没有岛屿，则返回面积为 0 。 
# 
#  
# 
#  示例 1： 
# 
#  
# 
#  
# 输入: grid = [[0,0,1,0,0,0,0,1,0,0,0,0,0],[0,0,0,0,0,0,0,1,1,1,0,0,0],[0,1,1,0,1
# ,0,0,0,0,0,0,0,0],[0,1,0,0,1,1,0,0,1,0,1,0,0],[0,1,0,0,1,1,0,0,1,1,1,0,0],[0,0,0
# ,0,0,0,0,0,0,0,1,0,0],[0,0,0,0,0,0,0,1,1,1,0,0,0],[0,0,0,0,0,0,0,1,1,0,0,0,0]]
# 输出: 6
# 解释: 对于上面这个给定矩阵应返回 6。注意答案不应该是 11 ，因为岛屿只能包含水平或垂直的四个方向的 1 。 
# 
#  示例 2： 
# 
#  
# 输入: grid = [[0,0,0,0,0,0,0,0]]
# 输出: 0 
# 
#  
# 
#  提示： 
# 
#  
#  m == grid.length 
#  n == grid[i].length 
#  1 <= m, n <= 50 
#  grid[i][j] is either 0 or 1 
#  
# 
#  
# 
#  注意：本题与主站 695 题相同： https://leetcode-cn.com/problems/max-area-of-island/ 
# 
#  Related Topics 深度优先搜索 广度优先搜索 并查集 数组 矩阵 👍 104 👎 0

from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
# todo dfs,bfs，之后写一下
class Solution:
    def maxAreaOfIsland1(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])
        #         dfs
        visited = set()
        res = 0

        # 返回的是岛屿的面积
        def dfs(grd, i, j):
            #             越界的情况就直接返回
            if i < 0 or i >= m or j < 0 or j >= n or (i, j) in visited or grd[i][j] == 0:
                return 0
            visited.add((i, j))
            a = dfs(grd, i + 1, j)
            b = dfs(grd, i - 1, j)
            c = dfs(grd, i, j + 1)
            d = dfs(grd, i, j - 1)
            return 1 + a + b + c + d

        for i in range(m):
            for j in range(n):
                if (i, j) not in visited and grid[i][j] == 1:
                    res = max(res, dfs(grid, i, j))
        return res

    def maxAreaOfIsland(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])
        # bfs
        visited = set()
        res = 0
        q = []
        dic = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        # 返回的是岛屿的面积
        for i in range(m):
            for j in range(n):
                if (i, j) not in visited and grid[i][j] == 1:
                    q.append((i, j))
                    visited.add((i, j))
                    tep = 1  # 本来就有1个面积
                    while q:
                        x, y = q.pop(0)
                        for diction in dic:
                            newi = x + diction[0]
                            newj = y + diction[1]
                            if (0 <= newi < m and 0 <= newj < n and (newi, newj)
                                    not in visited and grid[newi][newj] == 1):
                                q.append((newi, newj))
                                visited.add((newi, newj))
                                tep += 1
                    res = max(res, tep)

        return res


# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    grid = [[0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
            [0, 1, 1, 0, 1, 0, 0, 0, 0], [0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0],
            [0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0]]
    print(solution.maxAreaOfIsland(grid))
