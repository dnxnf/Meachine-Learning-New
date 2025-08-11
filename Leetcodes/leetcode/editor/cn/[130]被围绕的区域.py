# 给你一个 m x n 的矩阵 board ，由若干字符 'X' 和 'O' 组成，捕获 所有 被围绕的区域： 
# 
#  
#  连接：一个单元格与水平或垂直方向上相邻的单元格连接。 
#  区域：连接所有 'O' 的单元格来形成一个区域。 
#  围绕：如果您可以用 'X' 单元格 连接这个区域，并且区域中没有任何单元格位于 board 边缘，则该区域被 'X' 单元格围绕。 
#  
# 
#  通过 原地 将输入矩阵中的所有 'O' 替换为 'X' 来 捕获被围绕的区域。你不需要返回任何值。 
# 
#  
#  
#  
#  
#  
# 
#  示例 1： 
# 
#  
#  输入：board = [["X","X","X","X"],["X","O","O","X"],["X","X","O","X"],["X","O",
# "X","X"]] 
#  
# 
#  输出：[["X","X","X","X"],["X","X","X","X"],["X","X","X","X"],["X","O","X","X"]] 
# 
# 
#  解释： 
#  
#  在上图中，底部的区域没有被捕获，因为它在 board 的边缘并且不能被围绕。 
# 
#  示例 2： 
# 
#  
#  输入：board = [["X"]] 
#  
# 
#  输出：[["X"]] 
# 
#  
# 
#  提示： 
# 
#  
#  m == board.length 
#  n == board[i].length 
#  1 <= m, n <= 200 
#  board[i][j] 为 'X' 或 'O' 
#  
# 
#  Related Topics 深度优先搜索 广度优先搜索 并查集 数组 矩阵 👍 1220 👎 0

from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
# favour dfs,bfs,ufind都写一下
class Solution:
    def solve(self, board: List[List[str]]) -> None:
        """
        Do not return anything, modify board in-place instead.
        """
        if not board:
            return
        m, n = len(board), len(board[0])

        # 标记所有与边缘相连的'O'
        def dfs(i, j):
            if 0 <= i < m and 0 <= j < n and board[i][j] == 'O':
                board[i][j] = 'T'  # 临时标记
                dfs(i + 1, j)
                dfs(i - 1, j)
                dfs(i, j + 1)
                dfs(i, j - 1)
            # 这里隐含了else情况的自动返回
            # Python函数在没有return时会自动返回None

        # 从边缘开始DFS
        for i in range(m):
            if board[i][0] == 'O':
                dfs(i, 0)
            if board[i][n - 1] == 'O':
                dfs(i, n - 1)
        for j in range(n):
            if board[0][j] == 'O':
                dfs(0, j)
            if board[m - 1][j] == 'O':
                dfs(m - 1, j)


        # 修改内部未被标记的'O'，并恢复被标记的
        for i in range(m):
            for j in range(n):
                if board[i][j] == 'O':
                    board[i][j] = 'X'
                elif board[i][j] == 'T':
                    board[i][j] = 'O'

    def solve2(self, board: List[List[str]]) -> None:
        #         bfs
        m, n = len(board), len(board[0])
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        queue = []
        # 把每个边缘的O都记下来
        for i in range(m):
            for j in range(n):
                if board[i][j] == 'O' and (i == 0 or i == m - 1 or j == 0 or j == n - 1):
                    board[i][j] = 'T'
                    queue.append((i, j))
        # 只从边缘的开始修改
        while queue:
            i, j = queue.pop(0)
            for direction in directions:
                x, y = i + direction[0], j + direction[1]
                if 0 <= x < m and 0 <= y < n and board[x][y] == 'O':
                    board[x][y] = 'T'
                    queue.append((x, y))

        for i in range(m):
            for j in range(n):
                if board[i][j] == 'O':
                    board[i][j] = 'X'
                elif board[i][j] == 'T':
                    board[i][j] = 'O'

    def solve3(self, board: List[List[str]]) -> None:
        # 并查集实现,很慢
        if not board:
            return

        m, n = len(board), len(board[0])
        if m <= 2 or n <= 2:
            return
        parent = {}

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]  # 路径压缩
                x = parent[x]
            return x

        def union(x, y):
            rootX = find(x)
            rootY = find(y)
            if rootX != rootY:
                parent[rootX] = rootY

        # 虚拟安全节点（用特殊坐标表示）
        dummy = (-1, -1)
        parent[dummy] = dummy

        # 初始化所有'O'节点的父节点
        for i in range(m):
            for j in range(n):
                if board[i][j] == 'O':
                    parent[(i, j)] = (i, j)

        # 将边缘'O'连接到dummy
        for i in range(m):
            for j in [0, n - 1]:  # 左右两列
                if board[i][j] == 'O':
                    union((i, j), dummy)
        for j in range(n):
            for i in [0, m - 1]:  # 上下两行
                if board[i][j] == 'O':
                    union((i, j), dummy)

        # 连接相邻的'O'
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for i in range(1, m - 1):
            for j in range(1, n - 1):
                if board[i][j] == 'O':
                    for di, dj in directions:
                        ni, nj = i + di, j + dj
                        if board[ni][nj] == 'O':
                            union((i, j), (ni, nj))

        # 捕获被围绕的区域
        for i in range(1, m - 1):
            for j in range(1, n - 1):
                if board[i][j] == 'O' and find((i, j)) != find(dummy):
                    board[i][j] = 'X'


# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    board = [["X", "X", "X", "X"], ["X", "O", "O", "X"], ["X", "X", "O", "X"], ["X", "O", "X", "X"]]
    # board = [["X"]]
    # board = [["O", "O", "O"], ["O", "O", "O"], ["O", "O", "O"]]
    for i in range(len(board)):
        print(board[i])
    solution.solve(board)
    print('--------------------')
    for i in range(len(board)):
        print(board[i])
