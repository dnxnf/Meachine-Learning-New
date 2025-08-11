# 给你一个由 '1'（陆地）和 '0'（水）组成的的二维网格，请你计算网格中岛屿的数量。 
# 
#  岛屿总是被水包围，并且每座岛屿只能由水平方向和/或竖直方向上相邻的陆地连接形成。 
# 
#  此外，你可以假设该网格的四条边均被水包围。 
# 
#  
# 
#  示例 1： 
# 
#  
# 输入：grid = [
#   ["1","1","1","1","0"],
#   ["1","1","0","1","0"],
#   ["1","1","0","0","0"],
#   ["0","0","0","0","0"]
# ]
# 输出：1
#  
# 
#  示例 2： 
# 
#  
# 输入：grid = [
#   ["1","1","0","0","0"],
#   ["1","1","0","0","0"],
#   ["0","0","1","0","0"],
#   ["0","0","0","1","1"]
# ]
# 输出：3
#  
# 
#  
# 
#  提示： 
# 
#  
#  m == grid.length 
#  n == grid[i].length 
#  1 <= m, n <= 300 
#  grid[i][j] 的值为 '0' 或 '1' 
#  
# 
#  Related Topics 深度优先搜索 广度优先搜索 并查集 数组 矩阵 👍 2777 👎 0
from collections import deque
from typing import List, Optional


# favour 并查集的个数，DFS，bfs
# leetcode submit region begin(Prohibit modification and deletion)
class unionFind:
    def __init__(self, n):
        self.fa = [i for i in range(n)]
        self.cnt = 0

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

    # def set_count(self, count):
    #     self.cnt = count


class Solution:

    def numIslands1(self, grid: List[List[str]]) -> int:
        # 并查集
        m, n = len(grid), len(grid[0])
        uf = unionFind(m * n)
        cnt = 0

        for i in range(m):
            for j in range(n):
                if grid[i][j] == '1':
                    # 下面或右边
                    if i + 1 < len(grid) and grid[i + 1][j] == '1':
                        uf.union(i * n + j, (i + 1) * n + j)
                        # 不能这样写，会有重复合并的
                        # cnt -= 1
                        # print('下面,减1后', cnt)
                    if j + 1 < len(grid[0]) and grid[i][j + 1] == '1':
                        uf.union(i * n + j, i * n + j + 1)
        # 定义一个集合，集合里面是根节点
        # 从头遍历，如果是1，就把它的根节点加进去，看一共有几个根节点
        res = set()
        for i in range(m):
            for j in range(n):
                if grid[i][j] == '1':
                    idx = i * n + j
                    root = uf.find(idx)
                    res.add(root)  # 把根节点加进去,根节点都一样，所以只加一次

        return len(res)

    def numIsland2(self, grid: List[List[str]]) -> int:
        # 优化的dfs方法，使用set代替list，减少了时间复杂度
        # 使用set数组之后已经可以了，然后再将visited访问的1变成0,速度更快了一点
        m, n = len(grid), len(grid[0])
        #  使用dfs
        visited = set()
        cnt = 0

        # 所以visited就是把与这个1相连的全都加进去
        def dfs(grd, i, j, visit):
            if i < 0 or i >= m or j < 0 or j >= n \
                    or grd[i][j] == '0' or (i, j) in visit:
                return
            visit.add((i, j))
            grid[i][j] = '0'
            dfs(grd, i - 1, j, visit)
            dfs(grd, i + 1, j, visit)
            dfs(grd, i, j - 1, visit)
            dfs(grd, i, j + 1, visit)

        # 遇到一个1开始深搜，深搜到的1全都加到visited里面，加完之后cnt++
        for i in range(m):
            for j in range(n):
                if grid[i][j] == '1' and (i, j) not in visited:
                    cnt += 1
                    dfs(grid, i, j, visited)
        return cnt

    def numIslands(self, grid: List[List[str]]) -> int:
        # bfs,四个方向，上下左右，广度优先搜索，队列
        # 先把1变成0，避免重复搜索，然后广度优先搜索，遇到1就把它周围的1都变成0
        # 这样就能把所有的1都变成0，然后再把0变成1，然后再广度优先搜索，直到队列为空

        if not grid:
            return 0
        m, n = len(grid), len(grid[0])
        res = 0
        dic = [(0, 1), (1, 0), (-1, 0), (0, -1)]
        for i in range(m):
            for j in range(n):
                if grid[i][j] == "1":
                    # 置其为0，避免重复搜索
                    grid[i][j] = "0"
                    # queue = deque([i, j]),这个错了，i,j是元组，两两一组
                    queue = deque([(i, j)])
                    while queue:
                        # 没有这个会死循环
                        a, b = queue.popleft()
                        #  有元素的时候，遍历上下左右
                        for direct in dic:
                            newi = int(a) + direct[0]
                            newj = int(b) + direct[1]
                            if 0 <= newi < m and 0 <= newj < n and grid[newi][newj] == "1":
                                grid[newi][newj] = "0"
                                queue.append((newi, newj))
                    res = res + 1
        return res
        # leetcode submit region end(Prohibit modification and deletion)


if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    grid = [["1", "1", "1", "1", "0"],
            ["1", "1", "0", "1", "0"],
            ["1", "1", "0", "0", "0"],
            ["0", "0", "0", "0", "1"]]
    print(solution.numIslands(grid))
