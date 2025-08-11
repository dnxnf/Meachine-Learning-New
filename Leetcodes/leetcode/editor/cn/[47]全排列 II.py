# 给定一个可包含重复数字的序列 nums ，按任意顺序 返回所有不重复的全排列。 
# 
#  
# 
#  示例 1： 
# 
#  
# 输入：nums = [1,1,2]
# 输出：
# [[1,1,2],
#  [1,2,1],
#  [2,1,1]]
#  
# 
#  示例 2： 
# 
#  
# 输入：nums = [1,2,3]
# 输出：[[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]
#  
# 
#  
# 
#  提示： 
# 
#  
#  1 <= nums.length <= 8 
#  -10 <= nums[i] <= 10 
#  
# 
#  Related Topics 数组 回溯 排序 👍 1718 👎 0

from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    def permuteUnique(self, nums: List[int]) -> List[List[int]]:
        # favour 回溯法 待重复数字的全排列
        res = []
        path = []

        # 回溯
        def backtrack(num, visited):
            # 返回条件，达到条件了再加
            if len(path) == len(num):
                res.append(path[:])
                return

            for i in range(len(num)):
                # 相等的时候i-1却不在里面，说明这个之前选过了
                if i >= 1 and num[i] == num[i - 1] and (i-1) not in visited:
                    continue
                # 如果当前的i还没有加进去
                if i not in visited:
                    visited.append(i)
                    path.append(num[i])
                    backtrack(num, visited)
                    visited.remove(i)
                    path.pop()
        nums.sort()
        backtrack(nums, [])
        return res


# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution.permuteUnique([1, 1, 2]))
