# 丑数 就是只包含质因数 2、3 和 5 的 正 整数。 
# 
#  给你一个整数 n ，请你判断 n 是否为 丑数 。如果是，返回 true ；否则，返回 false 。 
# 
#  
# 
#  示例 1： 
# 
#  
# 输入：n = 6
# 输出：true
# 解释：6 = 2 × 3 
# 
#  示例 2： 
# 
#  
# 输入：n = 1
# 输出：true
# 解释：1 没有质因数。 
# 
#  示例 3： 
# 
#  
# 输入：n = 14
# 输出：false
# 解释：14 不是丑数，因为它包含了另外一个质因数 7 。
#  
# 
#  
# 
#  提示： 
# 
#  
#  -2³¹ <= n <= 2³¹ - 1 
#  
# 
#  Related Topics 数学 👍 491 👎 0

from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    def isUgly(self, n: int) -> bool:
        if n <= 0:
            return False
        for i in [2, 3, 5]:
            while n % i == 0:
                n //= i
        return n == 1


# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution.isUgly(14))
