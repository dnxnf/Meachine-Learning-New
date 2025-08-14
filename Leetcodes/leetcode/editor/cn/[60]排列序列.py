# 给出集合 [1,2,3,...,n]，其所有元素共有 n! 种排列。 
# 
#  按大小顺序列出所有排列情况，并一一标记，当 n = 3 时, 所有排列如下： 
# 
#  
#  "123" 
#  "132" 
#  "213" 
#  "231" 
#  "312" 
#  "321" 
#  
# 
#  给定 n 和 k，返回第 k 个排列。 
# 
#  
# 
#  示例 1： 
# 
#  
# 输入：n = 3, k = 3
# 输出："213"
#  
# 
#  示例 2： 
# 
#  
# 输入：n = 4, k = 9
# 输出："2314"
#  
# 
#  示例 3： 
# 
#  
# 输入：n = 3, k = 1
# 输出："123"
#  
# 
#  
# 
#  提示： 
# 
#  
#  1 <= n <= 9 
#  1 <= k <= n! 
#  
# 
#  Related Topics 递归 数学 👍 879 👎 0
from functools import lru_cache
from math import factorial
from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    def getPermutation1(self, n: int, k: int) -> str:
        # 超时
        res = []
        nums = list(range(1, n + 1))

        def backtrack(path):
            if len(res) == k:
                return
            if len(path) == n:
                res.append(''.join(map(str, path)))
                return
            for num in nums:
                if num not in path:
                    backtrack(path + [num])

        backtrack([])
        return res[-1]

    def getPermutation(self, n: int, k: int) -> str:
        nums = list(range(1, n + 1))  # [1, 2, ..., n]
        res = []
        k -= 1  # 转换为 0-based 索引

        for i in range(n, 0, -1):
            # 计算当前位的阶乘
            fact = factorial(i - 1)
            # 确定当前位的数字索引
            idx = k // fact
            res.append(str(nums.pop(idx)))
            # 更新 k
            k %= fact

        return ''.join(res)

# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution.getPermutation(3, 3))
