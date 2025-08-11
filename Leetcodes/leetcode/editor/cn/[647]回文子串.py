# 给你一个字符串 s ，请你统计并返回这个字符串中 回文子串 的数目。 
# 
#  回文字符串 是正着读和倒过来读一样的字符串。 
# 
#  子字符串 是字符串中的由连续字符组成的一个序列。 
# 
#  
# 
#  示例 1： 
# 
#  
# 输入：s = "abc"
# 输出：3
# 解释：三个回文子串: "a", "b", "c"
#  
# 
#  示例 2： 
# 
#  
# 输入：s = "aaa"
# 输出：6
# 解释：6个回文子串: "a", "a", "a", "aa", "aa", "aaa" 
# 
#  
# 
#  提示： 
# 
#  
#  1 <= s.length <= 1000 
#  s 由小写英文字母组成 
#  
# 
#  Related Topics 双指针 字符串 动态规划 👍 1450 👎 0

from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
# favour 中心扩展法
class Solution:
    def countSubstrings1(self, s: str) -> int:
        n = len(s)
        res = 0
        for i in range(n):
            # 枚举以i为中心的回文子串,奇数
            left, right = i, i
            while left >= 0 and right < n and s[left] == s[right]:
                res += 1
                left -= 1
                right += 1
            # 枚举以i为中心的回文子串,偶数
            left, right = i, i + 1
            while left >= 0 and right < n and s[left] == s[right]:
                res += 1
                left -= 1
                right += 1
        return res

    def countSubstrings(self, s: str) -> int:
        '''
        定义状态：dp[i][j]表示字符串s从索引i到j的子串是否是回文串。
        转移方程：
        如果s[i] == s[j]，且j - i ≤ 2，则dp[i][j] = True。（即子串长度为1、2或3）
        否则，如果s[i] == s[j]，且j - i > 2，则dp[i][j] = dp[i + 1][j - 1]。
        初始条件：
        dp[i][i] = True，表示长度为1的子串都是回文串。
        答案：
        遍历所有状态dp[i][j]，如果dp[i][j]为True，则说明s[i:j+1]是一个回文串，计数器count加1。
        初始化一个n×n的二维数组dp，所有值设为False。
        从字符串末尾开始倒序遍历（从下往上）。
        对于每个i，从i开始向右遍历（从左往右）。
        当s[i] == s[j]时：
        如果子串长度≤3（即j - i≤2），直接设为回文。
        否则检查去掉首尾字符后的子串是否是回文（dp[i + 1][j - 1]）。
        每次发现一个回文子串，计数器count加1。
        最后返回总数量count。
        '''
        n = len(s)
        dp = [[False] * n for _ in range(n)]
        count = 0

        for i in range(n - 1, -1, -1):  # 从下往上遍历
            for j in range(i, n):  # 从左往右遍历
                if s[i] == s[j]:
                    if j - i <= 2 or dp[i + 1][j - 1]:
                        dp[i][j] = True
                        count += 1

        return count


# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution.countSubstrings("aaa"))
