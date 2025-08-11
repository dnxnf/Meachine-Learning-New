# 在给定的 m x n 网格
#  grid 中，每个单元格可以有以下三个值之一： 
# 
#  
#  值 0 代表空单元格； 
#  值 1 代表新鲜橘子； 
#  值 2 代表腐烂的橘子。 
#  
# 
#  每分钟，腐烂的橘子 周围 4 个方向上相邻 的新鲜橘子都会腐烂。 
# 
#  返回 直到单元格中没有新鲜橘子为止所必须经过的最小分钟数。如果不可能，返回 -1 。 
# 
#  
# 
#  示例 1： 
# 
#  
# 
#  
# 输入：grid = [[2,1,1],[1,1,0],[0,1,1]]
# 输出：4
#  
# 
#  示例 2： 
# 
#  
# 输入：grid = [[2,1,1],[0,1,1],[1,0,1]]
# 输出：-1
# 解释：左下角的橘子（第 2 行， 第 0 列）永远不会腐烂，因为腐烂只会发生在 4 个方向上。
#  
# 
#  示例 3： 
# 
#  
# 输入：grid = [[0,2]]
# 输出：0
# 解释：因为 0 分钟时已经没有新鲜橘子了，所以答案就是 0 。
#  
# 
#  
# 
#  提示： 
# 
#  
#  m == grid.length 
#  n == grid[i].length 
#  1 <= m, n <= 10 
#  grid[i][j] 仅为 0、1 或 2 
#  
# 
#  Related Topics 广度优先搜索 数组 矩阵 👍 1031 👎 0
from collections import deque
from typing import List, Optional
# favour bfs同时有多个方向的搜索,考虑边界情况，好题

# leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    def orangesRotting(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])
        q = deque()
        fresh = 0
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        # 统计新鲜橘子的数量，并初始化队列
        for i in range(m):
            for j in range(n):
                if grid[i][j] == 1:
                    fresh += 1
                elif grid[i][j] == 2:
                    q.append((i, j))

        # 如果没有新鲜橘子，直接返回 0
        if fresh == 0:
            return 0

        minutes = 0
        while q:
            # 每分钟处理当前队列中的所有橘子
            size = len(q)
            for _ in range(size):
                x, y = q.popleft()
                for dx, dy in directions:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < m and 0 <= ny < n and grid[nx][ny] == 1:
                        grid[nx][ny] = 2
                        fresh -= 1
                        q.append((nx, ny))
            # 只有腐烂了橘子才增加时间
            # 当前腐烂的已经向外扩散了，如果有新的橘子被腐烂了
            if q:
                minutes += 1

        return minutes if fresh == 0 else -1
# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    grid = [[2,1,1],[1,1,0],[0,1,1]]
    print(solution.orangesRotting(grid))
