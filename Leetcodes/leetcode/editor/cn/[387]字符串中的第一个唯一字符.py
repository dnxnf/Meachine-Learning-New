# 给定一个字符串 s ，找到 它的第一个不重复的字符，并返回它的索引 。如果不存在，则返回 -1 。 
# 
#  
# 
#  示例 1： 
# 
#  
# 输入: s = "leetcode"
# 输出: 0
#  
# 
#  示例 2: 
# 
#  
# 输入: s = "loveleetcode"
# 输出: 2
#  
# 
#  示例 3: 
# 
#  
# 输入: s = "aabb"
# 输出: -1
#  
# 
#  
# 
#  提示: 
# 
#  
#  1 <= s.length <= 10⁵ 
#  s 只包含小写字母 
#  
# 
#  Related Topics 队列 哈希表 字符串 计数 👍 778 👎 0

from typing import List, Optional

# leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    def firstUniqChar(self, s: str) -> int:
        dic = {}
        for i, c in enumerate(s):
            if c in dic:
                dic[c] = -1
            else:
                dic[c] = i
        for i, c in enumerate(s):
            if dic[c] != -1:
                return dic[c]
        return -1
# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution)