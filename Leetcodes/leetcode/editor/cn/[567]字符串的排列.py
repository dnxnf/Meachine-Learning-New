# 给你两个字符串 s1 和 s2 ，写一个函数来判断 s2 是否包含 s1 的 排列。如果是，返回 true ；否则，返回 false 。 
# 
#  换句话说，s1 的排列之一是 s2 的 子串 。 
# 
#  
# 
#  示例 1： 
# 
#  
# 输入：s1 = "ab" s2 = "eidbaooo"
# 输出：true
# 解释：s2 包含 s1 的排列之一 ("ba").
#  
# 
#  示例 2： 
# 
#  
# 输入：s1= "ab" s2 = "eidboaoo"
# 输出：false
#  
# 
#  
# 
#  提示： 
# 
#  
#  1 <= s1.length, s2.length <= 10⁴ 
#  s1 和 s2 仅包含小写字母 
#  
# 
#  Related Topics 哈希表 双指针 字符串 滑动窗口 👍 1057 👎 0
from itertools import permutations
from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    def checkInclusion(self, s1: str, s2: str) -> bool:
        # 滑动窗口
        # 时间复杂度：O(n)
        # 空间复杂度：O(1)
        # 滑动窗口的左右边界
        def get_cnt(s):
            cnt = {}
            for c in s:
                cnt[c] = cnt.get(c, 0) + 1
            return cnt

        left, right = 0, len(s1)
        cnt1 = get_cnt(s1)
        # cnt2 = {}
        while right <= len(s2):
            cnt2 = get_cnt(s2[left:right])
            if cnt1 == cnt2:
                return True
            right += 1
            left += 1
        return False
# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution.checkInclusion("adc", "dada"))
