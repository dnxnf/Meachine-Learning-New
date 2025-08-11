# 给定一个 m x n 的矩阵，如果一个元素为 0 ，则将其所在行和列的所有元素都设为 0 。请使用 原地 算法。 
# 
#  
#  
# 
#  
# 
#  示例 1： 
#  
#  
# 输入：matrix = [[1,1,1],[1,0,1],[1,1,1]]
# 输出：[[1,0,1],[0,0,0],[1,0,1]]
#  
# 
#  示例 2： 
#  
#  
# 输入：matrix = [[0,1,2,0],[3,4,5,2],[1,3,1,5]]
# 输出：[[0,0,0,0],[0,4,5,0],[0,3,1,0]]
#  
# 
#  
# 
#  提示： 
# 
#  
#  m == matrix.length 
#  n == matrix[0].length 
#  1 <= m, n <= 200 
#  -2³¹ <= matrix[i][j] <= 2³¹ - 1 
#  
# 
#  
# 
#  进阶： 
# 
#  
#  一个直观的解决方案是使用 O(mn) 的额外空间，但这并不是一个好的解决方案。 
#  一个简单的改进方案是使用 O(m + n) 的额外空间，但这仍然不是最好的解决方案。 
#  你能想出一个仅使用常量空间的解决方案吗？ 
#  
# 
#  Related Topics 数组 哈希表 矩阵 👍 1240 👎 0

from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    def setZeroes1(self, matrix: List[List[int]]) -> None:
        """
        Do not return anything, modify matrix in-place instead.
        """
        m, n = len(matrix), len(matrix[0])
        row_zero = False
        col_zero = False
        for i in range(m):
            for j in range(n):
                if matrix[i][j] == 0:
                    matrix[i][0] = 0
                    matrix[0][j] = 0
                    if i == 0:
                        row_zero = True
                    if j == 0:
                        col_zero = True
        for i in range(1, m):
            if matrix[i][0] == 0:
                for j in range(1, n):
                    matrix[i][j] = 0
        for j in range(1, n):
            if matrix[0][j] == 0:
                for i in range(1, m):
                    matrix[i][j] = 0
        if row_zero:
            for j in range(n):
                matrix[0][j] = 0
        if col_zero:
            for i in range(m):
                matrix[i][0] = 0

    def setZeroes(self, matrix: List[List[int]]) -> None:
        m, n = len(matrix), len(matrix[0])
        tep = [[0] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                if matrix[i][j] == 0:
                    for k in range(m):
                        tep[k][j] = 1
                    for k in range(n):
                        tep[i][k] = 1
        for i in range(m):
            for j in range(n):
                if tep[i][j] == 1:
                    matrix[i][j] = 0


# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution)
