# 给定一个由 0 和 1 组成的矩阵 mat ，请输出一个大小相同的矩阵，其中每一个格子是 mat 中对应位置元素到最近的 0 的距离。 
# 
#  两个相邻元素间的距离为 1 。 
# 
#  
# 
#  示例 1： 
# 
#  
# 
#  
# 输入：mat = [[0,0,0],[0,1,0],[0,0,0]]
# 输出：[[0,0,0],[0,1,0],[0,0,0]]
#  
# 
#  示例 2： 
# 
#  
# 
#  
# 输入：mat = [[0,0,0],[0,1,0],[1,1,1]]
# 输出：[[0,0,0],[0,1,0],[1,2,1]]
#  
# 
#  
# 
#  提示： 
# 
#  
#  m == mat.length 
#  n == mat[i].length 
#  1 <= m, n <= 10⁴ 
#  1 <= m * n <= 10⁴ 
#  mat[i][j] is either 0 or 1. 
#  mat 中至少有一个 0 
#  
# 
#  Related Topics 广度优先搜索 数组 动态规划 矩阵 👍 995 👎 0

from typing import List, Optional
# favour bfs，检索与最近1的距离，偏难一点，逐层扩展,好题

# leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    def updateMatrix(self, mat: List[List[int]]) -> List[List[int]]:
        m, n = len(mat), len(mat[0])
        res = [[0] * n for _ in range(m)]
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        q = []
        for i in range(m):
            for j in range(n):
                if mat[i][j] == 0:
                    res[i][j] = 0
                    # 已经得到结果了
                    q.append((i, j))
                else:
                    res[i][j] = float('inf')
        # 从0出发，周围有1，则距离加一，加入队列，再吧这个1加入队列
        # 会先把0的处理完，再处理1，这样就保证了距离的计算是正确的
        while q:
            x, y = q.pop(0)
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                # 在矩阵内且未被访问过，新节点没有被访问过，距离+1，加入队列
                if 0 <= nx < m and 0 <= ny < n and res[nx][ny] == float('inf'):
                    res[nx][ny] = res[x][y] + 1
                    q.append((nx, ny))
        return res


# leetcode submit region end(Prohibit modification and deletion)


if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    nums = [[0, 0, 0], [0, 1, 0], [1, 1, 1]]
    print(solution.updateMatrix(nums))
