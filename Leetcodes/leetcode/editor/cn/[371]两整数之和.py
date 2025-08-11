# 给你两个整数 a 和 b ，不使用 运算符 + 和 - ，计算并返回两整数之和。 
# 
#  
# 
#  示例 1： 
# 
#  
# 输入：a = 1, b = 2
# 输出：3
#  
# 
#  示例 2： 
# 
#  
# 输入：a = 2, b = 3
# 输出：5
#  
# 
#  
# 
#  提示： 
# 
#  
#  -1000 <= a, b <= 1000 
#  
# 
#  Related Topics 位运算 数学 👍 766 👎 0

from typing import List, Optional

# leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    def getSum(self, a: int, b: int) -> int:
        mask = 0xFFFFFFFF  # 32-bit mask
        while b != 0:
            a, b = (a ^ b) & mask, ((a & b) << 1) & mask
        return a if a <= 0x7FFFFFFF else ~(a ^ mask)
# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution)