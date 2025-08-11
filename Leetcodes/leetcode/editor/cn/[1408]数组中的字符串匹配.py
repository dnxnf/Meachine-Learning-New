# 给你一个字符串数组 words ，数组中的每个字符串都可以看作是一个单词。请你按 任意 顺序返回 words 中是其他单词的 子字符串 的所有单词。 
# 
#  
# 
#  示例 1： 
# 
#  
# 输入：words = ["mass","as","hero","superhero"]
# 输出：["as","hero"]
# 解释："as" 是 "mass" 的子字符串，"hero" 是 "superhero" 的子字符串。
# ["hero","as"] 也是有效的答案。
#  
# 
#  示例 2： 
# 
#  
# 输入：words = ["leetcode","et","code"]
# 输出：["et","code"]
# 解释："et" 和 "code" 都是 "leetcode" 的子字符串。
#  
# 
#  示例 3： 
# 
#  
# 输入：words = ["blue","green","bu"]
# 输出：[]
#  
# 
#  
# 
#  提示： 
# 
#  
#  1 <= words.length <= 100 
#  1 <= words[i].length <= 30 
#  words[i] 仅包含小写英文字母。 
#  题目数据 保证 words 的每个字符串都是独一无二的。 
#  
# 
#  Related Topics 数组 字符串 字符串匹配 👍 114 👎 0

from typing import List, Optional

# leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    def stringMatching(self, words: List[str]) -> List[str]:
        res = []
        for i in range(len(words)):
            for j in range(len(words)):
                if i != j and words[i] in words[j]:
                    res.append(words[i])
                    break
        return res
# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution)