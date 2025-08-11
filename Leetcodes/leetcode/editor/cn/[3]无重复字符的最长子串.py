# 给定一个字符串 s ，请你找出其中不含有重复字符的 最长 子串 的长度。 
# 
#  
# 
#  示例 1: 
# 
#  
# 输入: s = "abcabcbb"
# 输出: 3 
# 解释: 因为无重复字符的最长子串是 "abc"，所以其长度为 3。
#  
# 
#  示例 2: 
# 
#  
# 输入: s = "bbbbb"
# 输出: 1
# 解释: 因为无重复字符的最长子串是 "b"，所以其长度为 1。
#  
# 
#  示例 3: 
# 
#  
# 输入: s = "pwwkew"
# 输出: 3
# 解释: 因为无重复字符的最长子串是 "wke"，所以其长度为 3。
#      请注意，你的答案必须是 子串 的长度，"pwke" 是一个子序列，不是子串。
#  
# 
#  
# 
#  提示： 
# 
#  
#  0 <= s.length <= 5 * 10⁴ 
#  s 由英文字母、数字、符号和空格组成 
#  
# 
#  Related Topics 哈希表 字符串 滑动窗口 👍 10851 👎 0
from collections import deque
from typing import List, Optional

# leetcode submit region begin(Prohibit modification and deletion)
from typing import Dict


class Solution:
    # 利用字符串当滑动窗口，空间占用大
    def lengthOfLongestSubstring1(self, s: str) -> int:
        # 滑动窗口

        current = ""
        maxn = 0
        left = 0
        for right in range(len(s)):
            while s[right] in current:
                current = current[1:]  # 移除最左边的字符
                left += 1
            #     移除完了，加入新的
            current += s[right]
            maxn = max(maxn, right - left + 1)
        return maxn

    def lengthOfLongestSubstring2(self, s: str) -> int:
        #         利用列表当滑动窗口
        current = []
        maxn = 0
        left = 0
        for right in range(len(s)):
            # 新的重复时
            while s[right] in current:
                current.remove(s[left])
                left += 1
            current.append(s[right])
            maxn = max(maxn, right - left + 1)
        return maxn

    def lengthOfLongestSubstring3(self, s: str) -> int:
        # 手写版1

        n = len(s)
        if n <= 1:
            return n
        cur = deque()
        maxn = 0
        left = 0
        for right, cha in enumerate(s):
            while cha in cur:
                cur.popleft()
                left += 1
            cur.append(cha)
            maxn = max(maxn, right - left + 1)
        return maxn

    def lengthOfLongestSubstring(self, s: str) -> int:
        # 用字典记录，记录每个字符第一次出现的位置，key是char，value是位置
        dic = {}
        left = 0
        # right = 0
        maxn = 0
        # favour 字典实现移动窗口
        # 可以少一次循环
        for right, chr in enumerate(s):
            if chr in dic and dic[chr] >= left:  # 如果字符在当前窗口内重复
                left = dic[chr] + 1  # 移动左边界到重复字符的下一个位置
            dic[chr] = right
            maxn = max(maxn, right - left + 1)
        return maxn


# leetcode submit region end(Prohibit modification and deletion)


if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution.lengthOfLongestSubstring("abcabcbb"))
