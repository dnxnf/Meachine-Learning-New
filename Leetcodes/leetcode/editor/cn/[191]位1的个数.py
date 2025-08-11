# 给定一个正整数 n，编写一个函数，获取一个正整数的二进制形式并返回其二进制表达式中 设置位 的个数（也被称为汉明重量）。 
# 
#  
# 
#  示例 1： 
# 
#  
# 输入：n = 11
# 输出：3
# 解释：输入的二进制串 1011 中，共有 3 个设置位。
#  
# 
#  示例 2： 
# 
#  
# 输入：n = 128
# 输出：1
# 解释：输入的二进制串 10000000 中，共有 1 个设置位。
#  
# 
#  示例 3： 
# 
#  
# 输入：n = 2147483645
# 输出：30
# 解释：输入的二进制串 1111111111111111111111111111101 中，共有 30 个设置位。 
# 
#  
# 
#  提示： 
# 
#  
#  1 <= n <= 2³¹ - 1 qwq
#  
# 
#  
#  
# 
#  
# 
#  进阶： 
# 
#  
#  如果多次调用这个函数，你将如何优化你的算法？ 
#  
# 
#  Related Topics 位运算 分治 👍 682 👎 0

from typing import List, Optional

# leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    def hammingWeight(self, n: int) -> int:
        # 是多少个1的个数
        count = 0
        # 循环n的二进制位
        num = bin(n)[2:]
        for i in num:
            # 如果该位是1，则count加1
            if i == '1':
                count += 1
        return count
# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution)