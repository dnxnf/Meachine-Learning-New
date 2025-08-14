# 给你一个整数 n ，请你在无限的整数序列 [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, ...] 中找出并返回第 n 位上的数字。
#  
# 
#  
# 
#  示例 1： 
# 
#  
# 输入：n = 3
# 输出：3
#  
# 
#  示例 2： 
# 
#  
# 输入：n = 11
# 输出：0
# 解释：第 11 位数字在序列 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, ... 里是 0 ，它是 10 的一部分。
#  
# 
#  
# 
#  提示： 
# 
#  
#  1 <= n <= 2³¹ - 1 
#  
# 
#  Related Topics 数学 二分查找 👍 429 👎 0

from typing import List, Optional

# leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    def findNthDigit(self, n: int) -> int:
        if n < 10:
            return n

        digit = 1  # 数字的位数（1, 2, 3...）
        start = 1  # 当前位数的最小数字（1, 10, 100...）
        count = 9  # 当前位数的数字总数（9, 90, 900...）

        # 1. 确定 n 所在的数字位数
        while n > count:
            n -= count
            digit += 1
            start *= 10
            count = 9 * start * digit

        # 2. 确定具体的数字
        num = start + (n - 1) // digit

        # 3. 确定数字中的具体某一位
        return int(str(num)[(n - 1) % digit])
        
# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution.findNthDigit(13))