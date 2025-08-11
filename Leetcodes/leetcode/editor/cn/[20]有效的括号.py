# 给定一个只包括 '('，')'，'{'，'}'，'['，']' 的字符串 s ，判断字符串是否有效。 
# 
#  有效字符串需满足： 
# 
#  
#  左括号必须用相同类型的右括号闭合。 
#  左括号必须以正确的顺序闭合。 
#  每个右括号都有一个对应的相同类型的左括号。 
#  
# 
#  
# 
#  示例 1： 
# 
#  
#  输入：s = "()" 
#  
# 
#  输出：true 
# 
#  示例 2： 
# 
#  
#  输入：s = "()[]{}" 
#  
# 
#  输出：true 
# 
#  示例 3： 
# 
#  
#  输入：s = "(]" 
#  
# 
#  输出：false 
# 
#  示例 4： 
# 
#  
#  输入：s = "([])" 
#  
# 
#  输出：true 
# 
#  
# 
#  提示： 
# 
#  
#  1 <= s.length <= 10⁴ 
#  s 仅由括号 '()[]{}' 组成 
#  
# 
#  Related Topics 栈 字符串 👍 4726 👎 0

from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    def isValid1(self, s: str) -> bool:
        dic = {'(': ')', '{': '}', '[': ']'}
        stack = []
        for i in s:
            if i in dic.keys():
                stack.append(i)
            elif i in dic.values() and len(stack) > 0:
                tep = stack.pop()
                if dic[tep] != i:
                    return False
            else:
                return False
        return len(stack) == 0

    def isValid2(self, s: str) -> bool:
        lst = []
        dic = {'(': ')', '[': ']', '{': '}'}
        for i, brt in enumerate(s):
            if brt in dic.keys():
                lst.append(brt)
            elif brt in dic.values():
                if lst and dic[lst[-1]] == brt:
                    lst.pop()
                else:
                    return False
            else:
                return False
        return len(lst) == 0

    def isValid(self, s: str) -> bool:
        # 一个栈，用来存储左括号，遇到右括号，则与栈顶元素匹配，匹配成功则出栈，否则返回False
        stack = []
        for i in s:
            if i in ['(', '{', '[']:
                stack.append(i)
            elif i in [')', '}', ']']:
                if not stack:
                    return False
                # 栈不为空，则匹配括号
                if i == ')' and stack[-1] != '(':
                    return False
                if i == '}' and stack[-1] != '{':
                    return False
                if i == ']' and stack[-1] != '[':
                    return False
                stack.pop()
            else:
                return False
        return not stack

# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution.isValid('()'))
