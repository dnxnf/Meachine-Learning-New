# 给你一个字符串 s，请你将 s 分割成一些 子串，使每个子串都是 回文串 。返回 s 所有可能的分割方案。 
# 
#  
# 
#  示例 1： 
# 
#  
# 输入：s = "aab"
# 输出：[["a","a","b"],["aa","b"]]
#  
# 
#  示例 2： 
# 
#  
# 输入：s = "a"
# 输出：[["a"]]
#  
# 
#  
# 
#  提示： 
# 
#  
#  1 <= s.length <= 16 
#  s 仅由小写英文字母组成 
#  
# 
#  Related Topics 字符串 动态规划 回溯 👍 2077 👎 0

from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    def partition(self, s: str) -> List[List[str]]:
        n = len(s)
        res = []

        def backtrack(start, path):
            if start == n:
                res.append(path[:])
                return
            for i in range(start, n):
                if self.is_palindrome(s[start:i + 1]):
                    path.append(s[start:i + 1])  # 如果是回文，加入当前路径
                    backtrack(i + 1, path)  # 递归处理剩余部分
                    path.pop()  # 回溯，移除最后添加的子串

        backtrack(0, [])
        return res

    def is_palindrome(self, s: str) -> bool:
        return s == s[::-1]


# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution.partition("aab"))
