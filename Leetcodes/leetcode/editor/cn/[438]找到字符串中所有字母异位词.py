# 给定两个字符串 s 和 p，找到 s 中所有 p 的 异位词 的子串，返回这些子串的起始索引。不考虑答案输出的顺序。 
# 
#  
# 
#  示例 1: 
# 
#  
# 输入: s = "cbaebabacd", p = "abc"
# 输出: [0,6]
# 解释:
# 起始索引等于 0 的子串是 "cba", 它是 "abc" 的异位词。
# 起始索引等于 6 的子串是 "bac", 它是 "abc" 的异位词。
#  
# 
#  示例 2: 
# 
#  
# 输入: s = "abab", p = "ab"
# 输出: [0,1,2]
# 解释:
# 起始索引等于 0 的子串是 "ab", 它是 "ab" 的异位词。
# 起始索引等于 1 的子串是 "ba", 它是 "ab" 的异位词。
# 起始索引等于 2 的子串是 "ab", 它是 "ab" 的异位词。
#  
# 
#  
# 
#  提示: 
# 
#  
#  1 <= s.length, p.length <= 3 * 10⁴ 
#  s 和 p 仅包含小写字母 
#  
# 
#  Related Topics 哈希表 字符串 滑动窗口 👍 1712 👎 0
from collections import defaultdict
from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    def IsAnagram(self, s, p) -> bool:
        if len(s)!= len(p):
            return False
        count = [0] * 26
        for i in range(len(s)):
            count[ord(s[i]) - ord('a')] += 1
            count[ord(p[i]) - ord('a')] -= 1
        for i in range(26):
            if count[i] != 0:
                return False
        return True
    def findAnagrams1(self, s: str, p: str) -> List[int]:
        # 遍历每个子串的起始位置，然后排序,还是超时
        res = []
        for i in range(len(s) - len(p) + 1):
            if self.IsAnagram(s[i:i+len(p)], p):
                res.append(i)
        return res
    def findAnagrams(self, s: str, p: str) -> List[int]:
        # 直接遍历子串，根据长度的滑动窗口，判断是否是异位词
        # 统计串的字符频率
        res = []
        len_p = len(p)
        len_s = len(s)
        # 长度不匹配
        if len_p > len_s:
            return res

        # 统计p的字符频率
        p_count = defaultdict(int)
        for char in p:
            p_count[char] += 1

        # 初始化滑动窗口的字符频率
        window_count = defaultdict(int)
        for i in range(len_p):
            char = s[i]
            window_count[char] += 1

        # 初始比较
        if window_count == p_count:
            res.append(0)

        # 滑动窗口
        for i in range(len_p, len_s):
            # 移除左边界的字符
            left_char = s[i - len_p]
            window_count[left_char] -= 1
            if window_count[left_char] == 0:
                del window_count[left_char]

            # 添加右边界的字符
            right_char = s[i]
            window_count[right_char] += 1

            # 比较当前窗口的字符频率
            if window_count == p_count:
                res.append(i - len_p + 1)

        return res
# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution.IsAnagram("asd", "das"))
