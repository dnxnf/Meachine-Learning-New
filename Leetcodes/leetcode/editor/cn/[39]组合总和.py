# 给你一个 无重复元素 的整数数组 candidates 和一个目标整数 target ，找出 candidates 中可以使数字和为目标数 target 的
#  所有 不同组合 ，并以列表形式返回。你可以按 任意顺序 返回这些组合。 
# 
#  candidates 中的 同一个 数字可以 无限制重复被选取 。如果至少一个数字的被选数量不同，则两种组合是不同的。 
# 
#  对于给定的输入，保证和为 target 的不同组合数少于 150 个。 
# 
#  
# 
#  示例 1： 
# 
#  
# 输入：candidates = [2,3,6,7], target = 7
# 输出：[[2,2,3],[7]]
# 解释：
# 2 和 3 可以形成一组候选，2 + 2 + 3 = 7 。注意 2 可以使用多次。
# 7 也是一个候选， 7 = 7 。
# 仅有这两种组合。 
# 
#  示例 2： 
# 
#  
# 输入: candidates = [2,3,5], target = 8
# 输出: [[2,2,2,2],[2,3,3],[3,5]] 
# 
#  示例 3： 
# 
#  
# 输入: candidates = [2], target = 1
# 输出: []
#  
# 
#  
# 
#  提示： 
# 
#  
#  1 <= candidates.length <= 30 
#  2 <= candidates[i] <= 40 
#  candidates 的所有元素 互不相同 
#  1 <= target <= 40 
#  
# 
#  Related Topics 数组 回溯 👍 3034 👎 0

from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
# from itertools import permutations
# favour 回溯法
class Solution:
    def combinationSum(self, cad: List[int], tar: int) -> List[List[int]]:
        # 当前选择的，剩余的金额，开始的地方
        def backtrack(combination, remaining, start):
            # combination：当前选择的商品组合
            # remaining：还需要凑的金额
            # start：从哪个商品开始尝试（避免重复组合）
            # 如果剩余金额正好为0，说明找到一组解,递归结束条件
            if remaining == 0:
                result.append(list(combination))
                return
            # 从start开始尝试每个商品
            for i in range(start, len(cad)):
                # 如果商品价格超过剩余金额，跳过（剪枝）
                if cad[i] > remaining:
                    # 已经排序，break和Continue都行，没有排序只能continue
                    break
                # 选择这个商品
                combination.append(cad[i])
                # 继续尝试用这个商品凑剩余金额（因为可以重复使用）
                backtrack(combination, remaining - cad[i], i)
                # 撤销选择，尝试其他可能性
                combination.pop()
        #   ---------- 回溯法 ----------
        result = []
        cad.sort()  # 先排序，方便剪枝
        backtrack([], tar, 0)
        return result
# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution.combinationSum(cad=[2, 3, 6, 7], tar=7))
