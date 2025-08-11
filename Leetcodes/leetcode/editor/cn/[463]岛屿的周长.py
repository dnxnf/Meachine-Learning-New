# 给定一个 row x col 的二维网格地图 grid ，其中：grid[i][j] = 1 表示陆地， grid[i][j] = 0 表示水域。 
# 
#  网格中的格子 水平和垂直 方向相连（对角线方向不相连）。整个网格被水完全包围，但其中恰好有一个岛屿（或者说，一个或多个表示陆地的格子相连组成的岛屿）。 
# 
#  岛屿中没有“湖”（“湖” 指水域在岛屿内部且不和岛屿周围的水相连）。格子是边长为 1 的正方形。网格为长方形，且宽度和高度均不超过 100 。计算这个岛屿
# 的周长。 
# 
#  
# 
#  示例 1： 
# 
#  
# 
#  
# 输入：grid = [[0,1,0,0],[1,1,1,0],[0,1,0,0],[1,1,0,0]]
# 输出：16
# 解释：它的周长是上面图片中的 16 个黄色的边 
# 
#  示例 2： 
# 
#  
# 输入：grid = [[1]]
# 输出：4
#  
# 
#  示例 3： 
# 
#  
# 输入：grid = [[1,0]]
# 输出：4
#  
# 
#  
# 
#  提示： 
# 
#  
#  row == grid.length 
#  col == grid[i].length 
#  1 <= row, col <= 100 
#  grid[i][j] 为 0 或 1 
#  
# 
#  Related Topics 深度优先搜索 广度优先搜索 数组 矩阵 👍 818 👎 0

from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    def islandPerimeter1(self, grid: List[List[int]]) -> int:
        #  上下左右有几个陆地，就4-n
        # 数组遍历法
        m, n = len(grid), len(grid[0])
        res = 0
        for i in range(m):
            for j in range(n):
                if grid[i][j] == 1:
                    res += 4
                    if i + 1 < m and grid[i + 1][j] == 1:
                        res -= 1
                    if i - 1 >= 0 and grid[i - 1][j] == 1:
                        res -= 1
                    if j + 1 < n and grid[i][j + 1] == 1:
                        res -= 1
                    if j - 1 >= 0 and grid[i][j - 1] == 1:
                        res -= 1
        return res

    def islandPerimeter2(self, grid: List[List[int]]) -> int:
        # dfs 递归检查每个陆地格子，遇到即加4，并且周围每有一个陆地就减一
        res = 0
        m, n = len(grid), len(grid[0])

        def dfs(i, j):
            nonlocal res
            if i < 0 or i >= m or j < 0 or j >= n or grid[i][j] == 0:
                res = res + 1
                return
            # make 标记是否访问过,已经访问过的不再重复访问
            if grid[i][j] == 2:
                return
            # res += 4
            grid[i][j] = 2
            dfs(i + 1, j)
            dfs(i - 1, j)
            dfs(i, j + 1)
            dfs(i, j - 1)

        for i in range(m):
            for j in range(n):
                if grid[i][j] == 1:
                    dfs(i, j)
                    break
        return res

    def islandPerimeter(self, grid: List[List[int]]) -> int:
        # bfs
        res = 0
        m, n = len(grid), len(grid[0])
        # favour 图的bfs的遍历公式了，生成四个方向，一个队列q或queue
        #  两层循环，然后找到条件就入队，然后while里面出队，再for四个方向
        # 然后遍历图，遇到一个根据题目条件标记一下，先入队再在遍历时候出队
        dict = [(0, 1), (1, 0), (-1, 0), (0, -1)]
        q = []
        for i in range(m):
            for j in range(n):
                if grid[i][j] == 1:
                    grid[i][j] = 2
                    # tep = 1
                    q.append((i, j))
                    while q:
                        i, j = q.pop(0)
                        for direct in dict:
                            newi = i + direct[0]
                            newj = j + direct[1]
                            # 越界或者碰到水就加一
                            if 0 > newi or 0 > newj or newi >= m or newj >= n or grid[newi][newj] == 0:
                                res += 1
        return res


# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution.islandPerimeter([[0, 1, 0, 0], [1, 1, 1, 0], [0, 1, 0, 0], [1, 1, 0, 0]]))
