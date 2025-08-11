# 你准备参加一场远足活动。给你一个二维 rows x columns 的地图 heights ，其中 heights[row][col] 表示格子 (row,
#  col) 的高度。一开始你在最左上角的格子 (0, 0) ，且你希望去最右下角的格子 (rows-1, columns-1) （注意下标从 0 开始编号）。你
# 每次可以往 上，下，左，右 四个方向之一移动，你想要找到耗费 体力 最小的一条路径。 
# 
#  一条路径耗费的 体力值 是路径上相邻格子之间 高度差绝对值 的 最大值 决定的。 
# 
#  请你返回从左上角走到右下角的最小 体力消耗值 。 
# 
#  
# 
#  示例 1： 
# 
#  
# 
#  
# 输入：heights = [[1,2,2],[3,8,2],[5,3,5]]
# 输出：2
# 解释：路径 [1,3,5,3,5] 连续格子的差值绝对值最大为 2 。
# 这条路径比路径 [1,2,2,2,5] 更优，因为另一条路径差值最大值为 3 。
#  
# 
#  示例 2： 
# 
#  
# 
#  
# 输入：heights = [[1,2,3],[3,8,4],[5,3,5]]
# 输出：1
# 解释：路径 [1,2,3,4,5] 的相邻格子差值绝对值最大为 1 ，比路径 [1,3,5,3,5] 更优。
#  
# 
#  示例 3： 
#  
#  
# 输入：heights = [[1,2,1,1,1],[1,2,1,2,1],[1,2,1,2,1],[1,2,1,2,1],[1,1,1,2,1]]
# 输出：0
# 解释：上图所示路径不需要消耗任何体力。
#  
# 
#  
# 
#  提示： 
# 
#  
#  rows == heights.length 
#  columns == heights[i].length 
#  1 <= rows, columns <= 100 
#  1 <= heights[i][j] <= 10⁶ 
#  
# 
#  Related Topics 深度优先搜索 广度优先搜索 并查集 数组 二分查找 矩阵 堆（优先队列） 👍 557 👎 0
import heapq
from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
# favour 普通队列实现和堆实现，图的最短体力消耗，ds说堆那个是dijkstra的变种
class Solution:
    def minimumEffortPath(self, heights: List[List[int]]) -> float:
        # 普通队列
        m, n = len(heights), len(heights[0])
        dp = [[float('inf')] * n for _ in range(m)]
        dp[0][0] = 0
        q = [(0, 0)]
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        while q:
            i, j = q.pop(0)
            # 广搜，遍历每个方向
            for di, dj in directions:
                ni, nj = i + di, j + dj
                if 0 <= ni < m and 0 <= nj < n:
                    # 临时距离是高度差绝对值
                    nd = max(dp[i][j], abs(heights[ni][nj] - heights[i][j]))
                    if nd < dp[ni][nj]:
                        dp[ni][nj] = nd
                        q.append((ni, nj))

        print(dp)
        return dp[m - 1][n - 1]

    def minimumEffortPath1(self, heights: List[List[int]]) -> int:
        # 优化，减少遍历层数，堆实现
        # 单源最短距离
        # note 优先队列（堆） 每个都会加进去，但是取出来先按最小的取，如果一个路径前面小，后面大了，
        #  就会先把之前更小的取出来。
        m, n = len(heights), len(heights[0])
        dist = [[float('inf')] * n for _ in range(m)]
        dist[0][0] = 0
        heap = [(0, 0, 0)]
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        while heap:
            d, x, y = heapq.heappop(heap)
            if x == m - 1 and y == n - 1:
                print(dist)
                return d  # 到达最后一个就输出
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < m and 0 <= ny < n:
                    nd = max(d, abs(heights[nx][ny] - heights[x][y]))
                    if nd < dist[nx][ny]:
                        dist[nx][ny] = nd
                        heapq.heappush(heap, (nd, nx, ny))
        # print(dist)
        return -1


# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution.minimumEffortPath([[1, 2, 2], [3, 8, 2], [5, 3, 5]]))
