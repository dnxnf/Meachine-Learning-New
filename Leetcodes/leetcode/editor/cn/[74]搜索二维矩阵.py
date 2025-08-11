# 给你一个满足下述两条属性的 m x n 整数矩阵： 
# 
#  
#  每行中的整数从左到右按非严格递增顺序排列。 
#  每行的第一个整数大于前一行的最后一个整数。 
#  
# 
#  给你一个整数 target ，如果 target 在矩阵中，返回 true ；否则，返回 false 。 
# 
#  
# 
#  示例 1： 
#  
#  
# 输入：matrix = [[1,3,5,7],[10,11,16,20],[23,30,34,60]], target = 3
# 输出：true
#  
# 
#  示例 2： 
#  
#  
# 输入：matrix = [[1,3,5,7],[10,11,16,20],[23,30,34,60]], target = 13
# 输出：false
#  
# 
#  
# 
#  提示： 
# 
#  
#  m == matrix.length 
#  n == matrix[i].length 
#  1 <= m, n <= 100 
#  -10⁴ <= matrix[i][j], target <= 10⁴ 
#  
# 
#  Related Topics 数组 二分查找 矩阵 👍 1053 👎 0

from typing import List, Optional

# leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        # 普通遍历
        # for row in matrix:
        #      if target in row:
        #          return True
        # return False

        # 二分查找
        for row in matrix:
            left, right = 0, len(row) - 1
            while left <= right:
                mid = (left + right) // 2
                if row[mid] == target:
                    return True
                elif row[mid] < target:
                    left = mid + 1
                #     比目标值大，左边界往左移
                else:
                    right = mid - 1
        return False
# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution)