# 给定一个字符串
#  s ，你需要反转字符串中每个单词的字符顺序，同时仍保留空格和单词的初始顺序。 
# 
#  
# 
#  示例 1： 
# 
#  
# 输入：s = "Let's take LeetCode contest"
# 输出："s'teL ekat edoCteeL tsetnoc"
#  
# 
#  示例 2: 
# 
#  
# 输入： s = "Mr Ding"
# 输出："rM gniD"
#  
# 
#  
# 
#  提示： 
# 
#  
#  1 <= s.length <= 5 * 10⁴ 
#  
#  s 包含可打印的 ASCII 字符。 
#  
#  s 不包含任何开头或结尾空格。 
#  
#  s 里 至少 有一个词。 
#  
#  s 中的所有单词都用一个空格隔开。 
#  
# 
#  Related Topics 双指针 字符串 👍 603 👎 0

from typing import List

# leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    def reverseWords(self, s: str) -> str:
        j = 0
        res = ""
        for i in range(len(s)):
            if s[i] == ' ':
                # 正确反向输出，不会越界
                print(s[j:i][::-1])
                res = res + s[j:i][::-1]+' '
                j = i + 1
            if i == len(s) - 1:
                res = res + s[j:i+1][::-1]
        return res
# leetcode submit region end(Prohibit modification and deletion)

# if __name__ == "__main__":
#     # 创建Solution实例
#     solution = Solution()
#     print(solution.reverseWords("Let's take LeetCode contest"))