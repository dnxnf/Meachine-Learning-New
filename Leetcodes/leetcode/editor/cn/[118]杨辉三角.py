# 给定一个非负整数 numRows，生成「杨辉三角」的前 numRows 行。 
# 
#  在「杨辉三角」中，每个数是它左上方和右上方的数的和。 
# 
#  
# 
#  
# 
#  示例 1: 
# 
#  
# 输入: numRows = 5
# 输出: [[1],[1,1],[1,2,1],[1,3,3,1],[1,4,6,4,1]]
#  
# 
#  示例 2: 
# 
#  
# 输入: numRows = 1
# 输出: [[1]]
#  
# 
#  
# 
#  提示: 
# 
#  
#  1 <= numRows <= 30 
#  
# 
#  Related Topics 数组 动态规划 👍 1257 👎 0

from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    def generate(self, num: int) -> List[List[int]]:

        if num == 1:
            return [[1]]
        if num == 2:
            return [[1], [1, 1]]
        res = [[1], [1, 1]]
        path = []
        for i in range(2, num):
            path.append(1)
            for j in range(1, i):
                path.append(res[-1][j - 1] + res[-1][j])
            path.append(1)
            res.append(path[:])
            # res.append(path.copy())
            path.clear()
        return res


# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution.generate(5))
