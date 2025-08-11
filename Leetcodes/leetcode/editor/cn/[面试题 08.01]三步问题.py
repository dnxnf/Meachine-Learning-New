# 三步问题。有个小孩正在上楼梯，楼梯有 n 阶台阶，小孩一次可以上 1 阶、2 阶或 3 阶。实现一种方法，计算小孩有多少种上楼梯的方式。结果可能很大，你需要
# 对结果模 1000000007。 
# 
#  示例 1： 
# 
#  
#  输入：n = 3 
#  输出：4
#  说明：有四种走法
#  
# 
#  示例 2： 
# 
#  
#  输入：n = 5
#  输出：13
#  
# 
#  提示: 
# 
#  
#  n 范围在[1, 1000000]之间 
#  
# 
#  Related Topics 记忆化搜索 数学 动态规划 👍 130 👎 0

from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    def waysToStep(self, n: int) -> int:
        if n == 0:
            return 0
        if n == 1:
            return 1
        if n == 2:
            return 2

        a, b, c = 1,1,2
        for i in range(3, n + 1):
            d = (a + b + c) % 1000000007
            a = b
            b = c
            c = d
        return c


# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution)
