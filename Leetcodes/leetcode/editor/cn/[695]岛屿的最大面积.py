# 给你一个大小为 m x n 的二进制矩阵 grid 。 
# 
#  岛屿 是由一些相邻的 1 (代表土地) 构成的组合，这里的「相邻」要求两个 1 必须在 水平或者竖直的四个方向上 相邻。你可以假设 grid 的四个边缘都
# 被 0（代表水）包围着。 
# 
#  岛屿的面积是岛上值为 1 的单元格的数目。 
# 
#  计算并返回 grid 中最大的岛屿面积。如果没有岛屿，则返回面积为 0 。 
# 
#  
# 
#  示例 1： 
#  
#  
# 输入：grid = [[0,0,1,0,0,0,0,1,0,0,0,0,0],[0,0,0,0,0,0,0,1,1,1,0,0,0],[0,1,1,0,1,
# 0,0,0,0,0,0,0,0],[0,1,0,0,1,1,0,0,1,0,1,0,0],[0,1,0,0,1,1,0,0,1,1,1,0,0],[0,0,0,
# 0,0,0,0,0,0,0,1,0,0],[0,0,0,0,0,0,0,1,1,1,0,0,0],[0,0,0,0,0,0,0,1,1,0,0,0,0]]
# 输出：6
# 解释：答案不应该是 11 ，因为岛屿只能包含水平或垂直这四个方向上的 1 。
#  
# 
#  示例 2： 
# 
#  
# 输入：grid = [[0,0,0,0,0,0,0,0]]
# 输出：0
#  
# 
#  
# 
#  提示： 
# 
#  
#  m == grid.length 
#  n == grid[i].length 
#  1 <= m, n <= 50 
#  grid[i][j] 为 0 或 1 
#  
# 
#  Related Topics 深度优先搜索 广度优先搜索 并查集 数组 矩阵 👍 1141 👎 0
from collections import deque
from typing import List, Optional


# favour 并查集加结构，DFS
# leetcode submit region begin(Prohibit modification and deletion)
class unionFind:
    def __init__(self, n):
        self.fa = [i for i in range(n)]

    def find(self, x):
        while self.fa[x] != x:
            self.fa[x] = self.fa[self.fa[x]]
            x = self.fa[x]
        return x

    def union(self, x, y):
        root1 = self.find(x)
        root2 = self.find(y)
        if root1 == root2:
            return False
        self.fa[root1] = root2
        return True

    def is_connected(self, x, y):
        return self.find(x) == self.find(y)


class Solution:
    def maxAreaOfIsland1(self, grid: List[List[int]]) -> int:
        # 周围一圈都是水，防止数组越界
        m = len(grid)
        n = len(grid[0])
        print(m, n)
        ufind = unionFind(m * n)
        for i in range(0, m):
            for j in range(0, n):
                if j + 1 < n and grid[i][j] == 1 and grid[i][j + 1] == 1:
                    ufind.union((i * n + j), (i * n + j + 1))  # 右边
                if i + 1 < m and grid[i][j] == 1 and grid[i + 1][j] == 1:
                    ufind.union((i * n + j), (i * n + j + n))  # 下边
        #                 应该只要右下，左和上按理说不用管，因为之前都加过了
        #         应该全都加进去了，然后查
        print(ufind.fa)
        # res = 0
        count = {}
        for i in range(0, m):
            for j in range(0, n):
                if grid[i][j] == 1:
                    # 找到这个的根
                    root = ufind.find(i * n + j)
                    #
                    count[root] = count.get(root, 0) + 1
        #           上面的代码等价于
        #             if root in count:
        #                 count[root] += 1
        #             else:
        #                 count[root] = 1
        return max(count.values()) if 0 < len(count) else 0

    #       遍历代码，加到并查集，最后找出序列最长的
    def maxAreaOfIsland2(self, grid: List[List[int]]) -> int:
        # 上面是并查集，这个是dfs
        if not grid:
            return 0
        m, n = len(grid), len(grid[0])
        max_area = 0

        def dfs(i, j):
            if 0 <= i < m and 0 <= j < n and grid[i][j] == 1:
                grid[i][j] = 0  # 标记为已访问
                # 关键是这个+1，每遇到一个1就加1
                return (1 + dfs(i + 1, j) +
                        dfs(i - 1, j) +
                        dfs(i, j + 1) +
                        dfs(i, j - 1))
            return 0

        for i in range(m):
            for j in range(n):
                if grid[i][j] == 1:
                    max_area = max(max_area, dfs(i, j))

        return max_area

    def maxAreaOfIsland(self, grid: List[List[int]]) -> int:
        #         bfs
        if not grid:
            return 0
        m, n = len(grid), len(grid[0])
        res = 0
        dict = [(0, 1), (1, 0), (-1, 0), (0, -1)]
        for i in range(m):
            for j in range(n):
                if grid[i][j] == 1:
                    grid[i][j] = 0
                    tep = 1
                    queue = deque([(i, j)])
                    # 队列里面有元素的时候，遍历其上下左右
                    while queue:
                        i, j = queue.popleft()
                        for direct in dict:
                            newi = i + direct[0]
                            newj = j + direct[1]
                            if (0 <= newi < m and 0 <= newj < n
                                    and grid[newi][newj] == 1):
                                grid[newi][newj] = 0
                                queue.append((newi, newj))
                                tep += 1
                    res = max(res, tep)
        return res
# leetcode submit region end(Prohibit modification and deletion)


if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    # grid = [[0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
    #         [0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    #         [0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0],
    #         [0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0],
    #         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    #         [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
    #         [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0]]
    grid = [[0, 0, 0, 0, 1, 1, 1, 0]]
    print(solution.maxAreaOfIsland(grid))
