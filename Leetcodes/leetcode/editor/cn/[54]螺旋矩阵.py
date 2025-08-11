# 给你一个 m 行 n 列的矩阵 matrix ，请按照 顺时针螺旋顺序 ，返回矩阵中的所有元素。 
# 
#  
# 
#  示例 1： 
#  
#  
# 输入：matrix = [[1,2,3],[4,5,6],[7,8,9]]
# 输出：[1,2,3,6,9,8,7,4,5]
#  
# 
#  示例 2： 
#  
#  
# 输入：matrix = [[1,2,3,4],[5,6,7,8],[9,10,11,12]]
# 输出：[1,2,3,4,8,12,11,10,9,5,6,7]
#  
# 
#  
# 
#  提示： 
# 
#  
#  m == matrix.length 
#  n == matrix[i].length 
#  1 <= m, n <= 10 
#  -100 <= matrix[i][j] <= 100 
#  
# 
#  Related Topics 数组 矩阵 模拟 👍 1962 👎 0

from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    def spiralOrder(self, matrix: List[List[int]]) -> List[int]:
        m, n = len(matrix), len(matrix[0])
        res = []
        top, bottom, left, right = 0, m - 1, 0, n - 1
        while top <= bottom and left <= right:
            # 向右
            for j in range(left, right + 1):
                res.append(matrix[top][j])
            top += 1
            # 向下
            for i in range(top, bottom + 1):
                res.append(matrix[i][right])
            right -= 1
            # 向左
            if top <= bottom:
                for j in range(right, left - 1, -1):
                    res.append(matrix[bottom][j])
                bottom -= 1
            # 向上
            if left <= right:
                for i in range(bottom, top - 1, -1):
                    res.append(matrix[i][left])
                left += 1
        return res
    # leetcode submit region end(Prohibit modification and deletion)


if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution.spiralOrder([[1, 2, 3], [4, 5, 6], [7, 8, 9]]))
    print(solution.spiralOrder([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]))
