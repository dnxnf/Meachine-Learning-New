# 一条包含字母 A-Z 的消息通过以下映射进行了 编码 ： 
# 
#  "1" -> 'A' "2" -> 'B' ... "25" -> 'Y' "26" -> 'Z' 
# 
#  然而，在 解码 已编码的消息时，你意识到有许多不同的方式来解码，因为有些编码被包含在其它编码当中（"2" 和 "5" 与 "25"）。 
# 
#  例如，"11106" 可以映射为： 
# 
#  
#  "AAJF" ，将消息分组为 (1, 1, 10, 6) 
#  "KJF" ，将消息分组为 (11, 10, 6) 
#  消息不能分组为 (1, 11, 06) ，因为 "06" 不是一个合法编码（只有 "6" 是合法的）。 
#  
# 
#  注意，可能存在无法解码的字符串。 
# 
#  给你一个只含数字的 非空 字符串 s ，请计算并返回 解码 方法的 总数 。如果没有合法的方式解码整个字符串，返回 0。 
# 
#  题目数据保证答案肯定是一个 32 位 的整数。 
# 
#  
# 
#  示例 1： 
# 
#  
# 输入：s = "12"
# 输出：2
# 解释：它可以解码为 "AB"（1 2）或者 "L"（12）。
#  
# 
#  示例 2： 
# 
#  
# 输入：s = "226"
# 输出：3
# 解释：它可以解码为 "BZ" (2 26), "VF" (22 6), 或者 "BBF" (2 2 6) 。
#  
# 
#  示例 3： 
# 
#  
# 输入：s = "06"
# 输出：0
# 解释："06" 无法映射到 "F" ，因为存在前导零（"6" 和 "06" 并不等价）。
#  
# 
#  
# 
#  提示： 
# 
#  
#  1 <= s.length <= 100 
#  s 只包含数字，并且可能包含前导零。 
#  
# 
#  Related Topics 字符串 动态规划 👍 1609 👎 0

from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    def numDecodings1(self, s: str) -> int:
        # dp[i] 表示 s[0:i+1] 解码的个数
        n = len(s)
        # a = f[i-2], b = f[i-1], c = f[i]
        a, b, c = 0, 1, 0
        for i in range(1, n + 1):
            c = 0
            if s[i - 1] != '0':
                c += b
            if i > 1 and s[i - 2] != '0' and int(s[i - 2:i]) <= 26:
                c += a
            a, b = b, c
        return c

    def numDecodings(self, s: str) -> int:
        n = len(s)
        # 特殊情况处理
        if n == 0:
            return 0
        if s[0] == '0':
            return 0
        if n == 1:
            return 1
        # dp[i] 表示 s[0:i+1] 解码的个数
        dp = [0] * (n + 1)
        dp[0] = 1
        dp[1] = 1
        # 开头不是0，则只有一种解码方式
        for i in range(2, n + 1):
            # 如果当前位是0，则只能从前一位和前两位来解码
            if s[i - 1] == '0':
                if s[i - 2] == '0' or int(s[i - 2:i]) > 26:
                    return 0
                dp[i] = dp[i - 2]
            #     如果当前位不是0，则有两种解码方式
            else:
                dp[i] = dp[i - 1]
                if s[i - 2] == '0' or int(s[i - 2:i]) > 26:
                    continue
                dp[i] += dp[i - 2]
        return dp[n]


# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution.numDecodings("12258"))
