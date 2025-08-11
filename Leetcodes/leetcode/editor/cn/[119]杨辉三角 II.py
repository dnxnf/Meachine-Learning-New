# 给定一个非负索引 rowIndex，返回「杨辉三角」的第 rowIndex 行。 
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
# 输入: rowIndex = 3
# 输出: [1,3,3,1]
#  
# 
#  示例 2: 
# 
#  
# 输入: rowIndex = 0
# 输出: [1]
#  
# 
#  示例 3: 
# 
#  
# 输入: rowIndex = 1
# 输出: [1,1]
#  
# 
#  
# 
#  提示: 
# 
#  
#  0 <= rowIndex <= 33 
#  
# 
#  
# 
#  进阶： 
# 
#  你可以优化你的算法到 O(rowIndex) 空间复杂度吗？ 
# 
#  Related Topics 数组 动态规划 👍 597 👎 0

from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    def getRow(self, rowIndex: int) -> List[int]:
        lst = []
        lst0 = [1]
        lst1 = [1, 1]
        lst2 = [1, 2, 1]
        lst.append(lst0)
        lst.append(lst1)
        lst.append(lst2)
        if rowIndex < 3:
            return lst[rowIndex]
        for i in range(3, rowIndex + 1):
            tep = []
            tep.append(1)
            for j in range(1, i):
                tep.append(lst[i - 1][j - 1] + lst[i - 1][j])
            tep.append(1)
            lst.append(tep)
        return lst[rowIndex]


# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution)
