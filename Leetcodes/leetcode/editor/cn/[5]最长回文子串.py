# 给你一个字符串 s，找到 s 中最长的 回文 子串。 
# 
#  
# 
#  示例 1： 
# 
#  
# 输入：s = "babad"
# 输出："bab"
# 解释："aba" 同样是符合题意的答案。
#  
# 
#  示例 2： 
# 
#  
# 输入：s = "cbbd"
# 输出："bb"
#  
# 
#  
# 
#  提示： 
# 
#  
#  1 <= s.length <= 1000 
#  s 仅由数字和英文字母组成 
#  
# 
#  Related Topics 双指针 字符串 动态规划 👍 7743 👎 0

from typing import List, Optional

# favour 回文子串，中心扩展法
# leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    def longestPalindrome(self, s: str) -> str:
        # 中心扩展法，从中间往两边扩展，对每一个都扩展，直到不好，然后记录长度，再与maxn比较
        if not s:
            return ""

        start = 0
        max_length = 1

        for i in range(len(s)):
            # 奇数长度的回文，以 s[i] 为中心
            len1 = self.expandAroundCenter(s, i, i)
            # 偶数长度的回文，以 s[i] 和 s[i+1] 为中心
            len2 = self.expandAroundCenter(s, i, i + 1)
            # 取较长的长度
            current_max = max(len1, len2)
            # 更新全局最大值
            if current_max > max_length:
                max_length = current_max
                start = i - (current_max - 1) // 2

        return s[start:start + max_length]

    def expandAroundCenter(self, s: str, left: int, right: int) -> int:
        # 从中心向两边扩展，返回回文串的长度
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        return right - left - 1

# leetcode submit region end(Prohibit modification and deletion)


if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution)
