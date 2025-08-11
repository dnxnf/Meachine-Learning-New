# 给你一个 32 位的有符号整数 x ，返回将 x 中的数字部分反转后的结果。 
# 
#  如果反转后整数超过 32 位的有符号整数的范围 [−2³¹, 231 − 1] ，就返回 0。 
# 假设环境不允许存储 64 位整数（有符号或无符号）。
# 
#  
# 
#  示例 1： 
# 
#  
# 输入：x = 123
# 输出：321
#  
# 
#  示例 2： 
# 
#  
# 输入：x = -123
# 输出：-321
#  
# 
#  示例 3： 
# 
#  
# 输入：x = 120
# 输出：21
#  
# 
#  示例 4： 
# 
#  
# 输入：x = 0
# 输出：0
#  
# 
#  
# 
#  提示： 
# 
#  
#  -2³¹ <= x <= 2³¹ - 1 
#  
# 
#  Related Topics 数学 👍 4092 👎 0

from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    def reverse1(self, x: int) -> int:
        # 检查第一位是否为负号，是的话从第二位开始反转
        if x < 0:
            x = -x  # -321 -> 321
            x = int(str(x)[::-1])  # 321 -> 123
            x = -x  # 123 -> -123
        else:
            x = int(str(x)[::-1])
        # 检查是否超过32位有符号整数范围
        if x > 2 ** 31 - 1 or x < -2 ** 31:
            return 0
        return x

    def reverse(self, x: int) -> int:
        if x == 0:
            return 0
        ans: str
        if x > 0:
            ans = str(x)[::-1]
        if x < 0:
            x = -x
            ans = '-' + str(x)[::-1]
        ans = int(ans)
        if ans > 2 ** 31 - 1 or ans < -2 ** 31:
            return 0
        return ans


# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution)
