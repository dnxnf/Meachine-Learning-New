# 给你一个字符串 columnTitle ，表示 Excel 表格中的列名称。返回 该列名称对应的列序号 。 
# 
#  例如： 
# 
#  
# A -> 1
# B -> 2
# C -> 3
# ...
# Z -> 26
# AA -> 27
# AB -> 28 
# ... 
# 
#  
# 
#  示例 1: 
# 
#  
# 输入: columnTitle = "A"
# 输出: 1
#  
# 
#  示例 2: 
# 
#  
# 输入: columnTitle = "AB"
# 输出: 28
#  
# 
#  示例 3: 
# 
#  
# 输入: columnTitle = "ZY"
# 输出: 701 
# 
#  
# 
#  提示： 
# 
#  
#  1 <= columnTitle.length <= 7 
#  columnTitle 仅由大写英文组成 
#  columnTitle 在范围 ["A", "FXSHRXW"] 内 
#  
# 
#  Related Topics 数学 字符串 👍 428 👎 0

from typing import List, Optional

# leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    def titleToNumber(self, columnTitle: str) -> int:
        # 相当于26进制的 ，a是1，z是26
        base = 1
        result = 0
        for i in range(len(columnTitle)-1, -1, -1):
            # ord()函数返回字符的ASCII码
            result += (ord(columnTitle[i]) - 64) * base
            base *= 26
        return result
# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution)