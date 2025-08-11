# 给你一个字符串 s 和一个字符串列表 wordDict 作为字典。如果可以利用字典中出现的一个或多个单词拼接出 s 则返回 true。 
# 
#  注意：不要求字典中出现的单词全部都使用，并且字典中的单词可以重复使用。 
# 
#  
# 
#  示例 1： 
# 
#  
# 输入: s = "leetcode", wordDict = ["leet", "code"]
# 输出: true
# 解释: 返回 true 因为 "leetcode" 可以由 "leet" 和 "code" 拼接成。
#  
# 
#  示例 2： 
# 
#  
# 输入: s = "applepenapple", wordDict = ["apple", "pen"]
# 输出: true
# 解释: 返回 true 因为 "applepenapple" 可以由 "apple" "pen" "apple" 拼接成。
#      注意，你可以重复使用字典中的单词。
#  
# 
#  示例 3： 
# 
#  
# 输入: s = "catsandog", wordDict = ["cats", "dog", "sand", "and", "cat"]
# 输出: false
#  
# 
#  
# 
#  提示： 
# 
#  
#  1 <= s.length <= 300 
#  1 <= wordDict.length <= 1000 
#  1 <= wordDict[i].length <= 20 
#  s 和 wordDict[i] 仅由小写英文字母组成 
#  wordDict 中的所有字符串 互不相同 
#  
# 
#  Related Topics 字典树 记忆化搜索 数组 哈希表 字符串 动态规划 👍 2785 👎 0
from functools import lru_cache
from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    # favour 动态规划挺好的题
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        # word_set = set(wordDict)
        n = len(s)

        # 深搜递归，从每个元素开始，如果能匹配上，则从后面继续匹配
        @lru_cache(None)
        def dfs(strs: str):
            # 返回的是一个结果
            if not strs:
                return True
            # 遍历所有可能的子串
            for i in range(1, len(strs) + 1):
                # 如果子串在字典中，则继续递归
                if strs[:i] in wordDict and dfs(strs[i:]):
                    # 如果能匹配上，则返回True
                    return True
            return False
        result = dfs(s)
        return result

    def wordBreak2(self, s: str, wordDict: List[str]) -> bool:
        word_set = set(wordDict)
        n = len(s)
        dp = [False] * (n + 1)
        dp[0] = True
        # 从1到结尾字符，再从0到当前字符，如果当前字符和前面的字符能组成字典中的单词，则当前字符也能组成字典中的单词
        for i in range(1, n + 1):
            for j in range(i):
                # 对于每个位置 i，检查所有可能的分割点 j（0 <= j < i），
                # 如果 dp[j] 为 True 且子字符串 s[j:i] 在字典中，则 dp[i] 为 True。
                if dp[j] and s[j:i] in word_set:
                    dp[i] = True
                    break
        return dp[n]


# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution.wordBreak("leetcode", ["leet", "code"]))
