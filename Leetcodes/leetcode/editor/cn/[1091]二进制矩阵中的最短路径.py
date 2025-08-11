# 给你一个 n x n 的二进制矩阵 grid 中，返回矩阵中最短 畅通路径 的长度。如果不存在这样的路径，返回 -1 。 
# 
#  二进制矩阵中的 畅通路径 是一条从 左上角 单元格（即，(0, 0)）到 右下角 单元格（即，(n - 1, n - 1)）的路径，该路径同时满足下述要求
# ： 
# 
#  
#  路径途经的所有单元格的值都是 0 。 
#  路径中所有相邻的单元格应当在 8 个方向之一 上连通（即，相邻两单元之间彼此不同且共享一条边或者一个角）。 
#  
# 
#  畅通路径的长度 是该路径途经的单元格总数。 
# 
#  
# 
#  示例 1： 
#  
#  
# 输入：grid = [[0,1],[1,0]]
# 输出：2
#  
# 
#  示例 2： 
#  
#  
# 输入：grid = [[0,0,0],[1,1,0],[1,1,0]]
# 输出：4
#  
# 
#  示例 3： 
# 
#  
# 输入：grid = [[1,0,0],[1,1,0],[1,1,0]]
# 输出：-1
#  
# 
#  
# 
#  提示： 
# 
#  
#  m == grid.length
#  n == grid[i].length 
#  1 <= n <= 100 
#  grid[i][j] 为 0 或 1 
#  
# 
#  Related Topics 广度优先搜索 数组 矩阵 👍 401 👎 0
from collections import deque
from typing import List, Optional


# favour 经典问题，图里面的最短联通路径，最短路径还是bfs，带权的最短路径用dijkstra
# leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    def shortestPathBinaryMatrix1(self, grid: List[List[int]]) -> int:
        # 回溯法,会超时,还有冗余代码，每次都要修改tep和used的值，可以直接将tep作为参数传递，避免修改
        n = len(grid)
        cnt = float('inf')
        directions = [(1, 1), (0, 1), (1, 0), (-1, 0), (0, -1), (-1, -1), (1, -1), (-1, 1)]
        tep = 1

        def dfs(x, y):
            nonlocal cnt, tep
            if x == n - 1 and y == n - 1:
                cnt = min(cnt, tep)
                return
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < n and 0 <= ny < n and grid[nx][ny] == 0:
                    grid[nx][ny] = 1
                    tep += 1
                    dfs(nx, ny)
                    tep -= 1
                    grid[nx][ny] = 0

        dfs(0, 0)
        return cnt if cnt < float('inf') else -1

    def shortestPathBinaryMatrix2(self, grid: List[List[int]]) -> int:
        # dfs,避免显式回溯，直接用参数记录当前路径长度
        # dfs,拼尽全力无法战胜
        if grid[0][0] != 0 or grid[-1][-1] != 0:
            return -1
        n = len(grid)
        directions = [(1, 1), (0, 1), (1, 0), (-1, 0), (0, -1), (-1, -1), (1, -1), (-1, 1)]
        cnt = float('inf')

        def dfs(x, y, step):
            nonlocal cnt
            if x == n - 1 and y == n - 1:
                cnt = min(cnt, step)
                return
            if step > cnt:
                return
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < n and 0 <= ny < n and grid[nx][ny] == 0:
                    # 访问过的节点标记为1，避免重复访问，少了一个visited数组
                    grid[nx][ny] = 1
                    dfs(nx, ny, step + 1)
                    grid[nx][ny] = 0

        grid[0][0] = 1
        dfs(0, 0, 1)
        return cnt if cnt < float('inf') else -1

    def shortestPathBinaryMatrix(self, grid: List[List[int]]) -> int:
        #  bfs, 广度优先搜索
        if grid[0][0] != 0 or grid[-1][-1] != 0:
            return -1
        n = len(grid)
        directions = [(0, 1), (1, 0), (1, 1), (-1, 0), (0, -1), (-1, -1), (1, -1), (-1, 1)]
        q = deque([(0, 0, 1)])  # 队列，元素为(x, y, step),得在[]里面写
        while q:
            x, y, step = q.popleft()
            if x == n - 1 and y == n - 1:
                return step
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < n and 0 <= ny < n and grid[nx][ny] == 0:
                    # 访问过的节点标记为1，避免重复访问，少了一个visited数组
                    grid[nx][ny] = 1
                    q.append((nx, ny, step + 1))
        return -1


# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution.shortestPathBinaryMatrix([[0, 0, 0], [1, 1, 0], [1, 1, 0]]))
    print(solution.shortestPathBinaryMatrix(
        [[0, 1, 1, 0, 0, 0], [0, 1, 0, 1, 1, 0], [0, 1, 1, 0, 1, 0], [0, 0, 0, 1, 1, 0], [1, 1, 1, 1, 1, 0],
         [1, 1, 1, 1, 1, 0]]))
    lists = [[0, 1, 1, 0, 0, 0], [0, 1, 0, 1, 1, 0], [0, 1, 1, 0, 1, 0], [0, 0, 0, 1, 1, 0], [1, 1, 1, 1, 1, 0],
             [1, 1, 1, 1, 1, 0]]

    for lst in lists:
        print(lst)
