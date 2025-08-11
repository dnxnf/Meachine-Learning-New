# 给你一个由 '('、')' 和小写字母组成的字符串 s。 
# 
#  你需要从字符串中删除最少数目的 '(' 或者 ')' （可以删除任意位置的括号)，使得剩下的「括号字符串」有效。 
# 
#  请返回任意一个合法字符串。 
# 
#  有效「括号字符串」应当符合以下 任意一条 要求： 
# 
#  
#  空字符串或只包含小写字母的字符串 
#  可以被写作 AB（A 连接 B）的字符串，其中 A 和 B 都是有效「括号字符串」 
#  可以被写作 (A) 的字符串，其中 A 是一个有效的「括号字符串」 
#  
# 
#  
# 
#  示例 1： 
# 
#  
# 输入：s = "lee(t(c)o)de)"
# 输出："lee(t(c)o)de"
# 解释："lee(t(co)de)" , "lee(t(c)ode)" 也是一个可行答案。
#  
# 
#  示例 2： 
# 
#  
# 输入：s = "a)b(c)d"
# 输出："ab(c)d"
#  
# 
#  示例 3： 
# 
#  
# 输入：s = "))(("
# 输出：""
# 解释：空字符串也是有效的
#  
# 
#  
# 
#  提示： 
# 
#  
#  1 <= s.length <= 10⁵ 
#  s[i] 可能是 '('、')' 或英文小写字母 
#  
# 
#  Related Topics 栈 字符串 👍 275 👎 0
from collections import deque
from typing import List, Optional

# leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    def minRemoveToMakeValid(self, s: str) -> str:
        lst = list(s)
        q = deque([])
        for i, c in enumerate(lst):
            if c == '(':
                # 存了索引才能在最后找到要删除的位置
                q.append(i)
            elif c == ')':
                if q and lst[q[-1]] == '(':
                    q.pop()
                else:
                    lst[i] = ''
            else:
                continue
        #   栈里面剩下的是不能正确匹配的索引
        while q:
            lst[q.pop()] = ''
        return ''.join(lst)

# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution.minRemoveToMakeValid("lee(t(c)o)de)"))