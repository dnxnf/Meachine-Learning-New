# 某班级考试成绩按非严格递增顺序记录于整数数组 scores，请返回目标成绩 target 的出现次数。 
# 
#  
# 
#  示例 1： 
# 
#  
# 输入: scores = [2, 2, 3, 4, 4, 4, 5, 6, 6, 8], target = 4
# 输出: 3 
# 
#  示例 2： 
# 
#  
# 输入: scores = [1, 2, 3, 5, 7, 9], target = 6
# 输出: 0 
# 
#  
# 
#  提示： 
# 
#  
#  0 <= scores.length <= 10⁵ 
#  -10⁹ <= scores[i] <= 10⁹ 
#  scores 是一个非递减数组 
#  -10⁹ <= target <= 10⁹ 
#  
# 
#  
# 
#  注意：本题与主站 34 题相同（仅返回值不同）：https://leetcode-cn.com/problems/find-first-and-last-
# position-of-element-in-sorted-array/ 
# 
#  
# 
#  Related Topics 数组 二分查找 👍 462 👎 0

from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    def countTarget1(self, scores: List[int], target: int) -> int:
        cnt = 0
        for score in scores:
            if score == target:
                cnt += 1
        return cnt

    def countTarget(self, scores: List[int], target: int) -> int:
        # 二分查找
        left, right = 0, len(scores) - 1
        cnt = 0
        while left <= right:
            mid = (left + right) // 2
            # 已经找到target了，向左右查找
            if scores[mid] == target:
                tepl, tepr = mid, mid + 1
                while tepl >= 0 and scores[tepl] == target:
                    tepl -= 1
                    cnt += 1
                while tepr < len(scores) and scores[tepr] == target:
                    tepr += 1
                    cnt += 1
                return cnt
            # 左半边有target
            elif scores[mid] < target:
                left = mid + 1
            # 右半边有target
            else:
                right = mid - 1
        return cnt


# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution.countTarget([2, 2, 3, 4, 4, 4, 5, 6, 6, 8], 4))
