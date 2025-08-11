# 如果在将所有大写字符转换为小写字符、并移除所有非字母数字字符之后，短语正着读和反着读都一样。则可以认为该短语是一个 回文串 。 
# 
#  字母和数字都属于字母数字字符。 
# 
#  给你一个字符串 s，如果它是 回文串 ，返回 true ；否则，返回 false 。 
# 
#  
# 
#  示例 1： 
# 
#  
# 输入: s = "A man, a plan, a canal: Panama"
# 输出：true
# 解释："amanaplanacanalpanama" 是回文串。
#  
# 
#  示例 2： 
# 
#  
# 输入：s = "race a car"
# 输出：false
# 解释："raceacar" 不是回文串。
#  
# 
#  示例 3： 
# 
#  
# 输入：s = " "
# 输出：true
# 解释：在移除非字母数字字符之后，s 是一个空字符串 "" 。
# 由于空字符串正着反着读都一样，所以是回文串。
#  
# 
#  
# 
#  提示： 
# 
#  
#  1 <= s.length <= 2 * 10⁵ 
#  s 仅由可打印的 ASCII 字符组成 
#  
# 
#  Related Topics 双指针 字符串 👍 822 👎 0

from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    def isPalindrome1(self, s: str) -> bool:
        lst = list(s.lower())
        # 用列表，减少内存消耗
        n = len(lst)
        res = []
        for i in range(n):
            if lst[i].isalnum():
                res.append(lst[i])
        # 判断是否为回文串
        print(res)
        return res == res[::-1]

    def isPalindrome(self, s: str) -> bool:
        # 双指针
        left, right = 0, len(s) - 1
        while left < right:
            # 跳过非字母数字字符
            while left < right and not s[left].isalnum():
                left += 1
            while left < right and not s[right].isalnum():
                right -= 1
            # 转化为小写字母
            if s[left].lower() != s[right].lower():
                return False
            left += 1
            right -= 1
        return True


# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution.isPalindrome("A man, a plan, a canal: Panama"))
