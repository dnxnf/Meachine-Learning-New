# 给你一个字符串数组，请你将 字母异位词 组合在一起。可以按任意顺序返回结果列表。 
# 
#  
# 
#  示例 1: 
# 
#  
#  输入: strs = ["eat", "tea", "tan", "ate", "nat", "bat"] 
#  
# 
#  输出: [["bat"],["nat","tan"],["ate","eat","tea"]] 
# 
#  解释： 
# 
#  
#  在 strs 中没有字符串可以通过重新排列来形成 "bat"。 
#  字符串 "nat" 和 "tan" 是字母异位词，因为它们可以重新排列以形成彼此。 
#  字符串 "ate" ，"eat" 和 "tea" 是字母异位词，因为它们可以重新排列以形成彼此。 
#  
# 
#  示例 2: 
# 
#  
#  输入: strs = [""] 
#  
# 
#  输出: [[""]] 
# 
#  示例 3: 
# 
#  
#  输入: strs = ["a"] 
#  
# 
#  输出: [["a"]] 
# 
#  
# 
#  提示： 
# 
#  
#  1 <= strs.length <= 10⁴ 
#  0 <= strs[i].length <= 100 
#  strs[i] 仅包含小写字母 
#  
# 
#  Related Topics 数组 哈希表 字符串 排序 👍 2321 👎 0
from collections import defaultdict
from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    def groupAnagrams1(self, strs: List[str]) -> List[List[str]]:
        ans = {}
        res = []
        path = []
        # 把一样的分组，分别存储，
        # 如果对元素分组，再把一样的价进去呢
        for i, s in enumerate(strs):
            # 先排序，再判断是否一样
            sorted_s = ''.join(sorted(s))
            # 记录的就是排序后字符串的下标了
            ans[i] = sorted_s
            # print(sorted_s)
        # 遍历字典，把相同的分组放到一起
        for k, v in ans.items():
            if v not in path:
                path.append(v)
                res.append([strs[k]])
            else:
                res[path.index(v)].append(strs[k])
        return res

    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        anagram_map = defaultdict(list)

        for s in strs:
            sorted_s = ''.join(sorted(s))
            anagram_map[sorted_s].append(s)

        return list(anagram_map.values())


# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution.groupAnagrams(["eat", "tea", "tan", "ate", "nat", "bat"]))
