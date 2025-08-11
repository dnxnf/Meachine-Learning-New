# 给你一个字符串表达式 s ，请你实现一个基本计算器来计算并返回它的值。 
# 
#  整数除法仅保留整数部分。 
# 
#  你可以假设给定的表达式总是有效的。所有中间结果将在 [-2³¹, 2³¹ - 1] 的范围内。 
# 
#  注意：不允许使用任何将字符串作为数学表达式计算的内置函数，比如 eval() 。 
# 
#  
# 
#  示例 1： 
# 
#  
# 输入：s = "3+2*2"
# 输出：7
#  
# 
#  示例 2： 
# 
#  
# 输入：s = " 3/2 "
# 输出：1
#  
# 
#  示例 3： 
# 
#  
# 输入：s = " 3+5 / 2 "
# 输出：5
#  
# 
#  
# 
#  提示： 
# 
#  
#  1 <= s.length <= 3 * 10⁵ 
#  s 由整数和算符 ('+', '-', '*', '/') 组成，中间由一些空格隔开 
#  s 表示一个 有效表达式 
#  表达式中的所有整数都是非负整数，且在范围 [0, 2³¹ - 1] 内 
#  题目数据保证答案是一个 32-bit 整数 
#  
# 
#  Related Topics 栈 数学 字符串 👍 851 👎 0

from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    def calculate1(self, s: str) -> int:
        stack = []
        num = 0
        sign = "+"
        for i in range(len(s)):
            if s[i].isdigit():
                num = num * 10 + int(s[i])
            if (not s[i].isdigit() and not s[i].isspace()) or i == len(s) - 1:
                if sign == "+":
                    stack.append(num)
                elif sign == "-":
                    stack.append(-num)
                elif sign == "*":
                    stack.append(stack.pop() * num)
                else:
                    stack.append(int(stack.pop() / num))
                sign = s[i]
                num = 0
        return sum(stack)

    def calculate(self, s: str) -> int:
        expr = s.replace('/', '//').replace(' ', '')
        # 使用 eval 计算，并返回整数结果
        return eval(expr)


# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution)
