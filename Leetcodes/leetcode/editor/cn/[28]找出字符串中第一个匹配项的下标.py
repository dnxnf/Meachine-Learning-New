# 给你两个字符串 haystack 和 needle ，请你在 haystack 字符串中找出 needle 字符串的第一个匹配项的下标（下标从 0 开始）。
# 如果 needle 不是 haystack 的一部分，则返回 -1 。 
# 
#  
# 
#  示例 1： 
# 
#  
# 输入：haystack = "sadbutsad", needle = "sad"
# 输出：0
# 解释："sad" 在下标 0 和 6 处匹配。
# 第一个匹配项的下标是 0 ，所以返回 0 。
#  
# 
#  示例 2： 
# 
#  
# 输入：haystack = "leetcode", needle = "leeto"
# 输出：-1
# 解释："leeto" 没有在 "leetcode" 中出现，所以返回 -1 。
#  
# 
#  
# 
#  提示： 
# 
#  
#  1 <= haystack.length, needle.length <= 10⁴ 
#  haystack 和 needle 仅由小写英文字符组成 
#  
# 
#  Related Topics 双指针 字符串 字符串匹配 👍 2420 👎 0

from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    def strStr1(self, haystack: str, needle: str) -> int:
        for i in range(len(haystack) - len(needle) + 1):
            if haystack[i:i + len(needle)] == needle:
                return i
        return -1

    def strStr(self, haystack: str, needle: str) -> int:
        m, n = len(haystack), len(needle)
        if n == 0:
            return 0
        if m < n:
            return -1
        for i in range(m - n + 1):
            if haystack[i:i + n] == needle:
                return i
        return -1

# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution)
