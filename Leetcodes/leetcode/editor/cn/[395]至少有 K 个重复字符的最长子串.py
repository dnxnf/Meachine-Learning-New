# 给你一个字符串 s 和一个整数 k ，请你找出 s 中的最长子串， 要求该子串中的每一字符出现次数都不少于 k 。返回这一子串的长度。 
# 
#  如果不存在这样的子字符串，则返回 0。 
# 
#  
# 
#  示例 1： 
# 
#  
# 输入：s = "aaabb", k = 3
# 输出：3
# 解释：最长子串为 "aaa" ，其中 'a' 重复了 3 次。
#  
# 
#  示例 2： 
# 
#  
# 输入：s = "ababbc", k = 2
# 输出：5
# 解释：最长子串为 "ababb" ，其中 'a' 重复了 2 次， 'b' 重复了 3 次。 
# 
#  
# 
#  提示： 
# 
#  
#  1 <= s.length <= 10⁴ 
#  s 仅由小写英文字母组成 
#  1 <= k <= 10⁵ 
#  
# 
#  Related Topics 哈希表 字符串 分治 滑动窗口 👍 975 👎 0

from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    def longestSubstring1(self, s: str, k: int) -> int:
        max_len = 0
        n = len(s)

        for unique in range(1, 27):  # 最多26种字符
            left = 0
            freq = [0] * 26
            count_at_least_k = 0
            total_unique = 0

            for right in range(n):
                char = s[right]
                idx = ord(char) - ord('a')
                if freq[idx] == 0:
                    total_unique += 1
                freq[idx] += 1
                if freq[idx] == k:
                    count_at_least_k += 1

                while total_unique > unique:
                    left_char = s[left]
                    left_idx = ord(left_char) - ord('a')
                    if freq[left_idx] == k:
                        count_at_least_k -= 1
                    freq[left_idx] -= 1
                    if freq[left_idx] == 0:
                        total_unique -= 1
                    left += 1

                if total_unique == unique and count_at_least_k == unique:
                    max_len = max(max_len, right - left + 1)

        return max_len
    def longestSubstring(self, s: str, k: int) -> int:
        if len(s) < k:
            return 0

            # 统计字符频率
        freq = {}
        for char in s:
            freq[char] = freq.get(char, 0) + 1

        # 找出所有无效字符（出现次数<k）
        invalid_chars = set()
        for char, count in freq.items():
            if count < k:
                invalid_chars.add(char)

        # 如果没有无效字符，整个字符串都满足条件
        if not invalid_chars:
            return len(s)

        max_len = 0
        start = 0
        n = len(s)

        # 遍历字符串，以无效字符为分割点
        for end in range(n):
            if s[end] in invalid_chars:
                # 只处理长度可能超过当前最大值的子串
                if end - start > max_len:
                    left_sub = self.longestSubstring(s[start:end], k)
                    max_len = max(max_len, left_sub)
                start = end + 1

        # 处理最后一个子串
        if n - start > max_len:
            right_sub = self.longestSubstring(s[start:], k)
            max_len = max(max_len, right_sub)

        return max_len
# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution.longestSubstring("aaabb", 3))
