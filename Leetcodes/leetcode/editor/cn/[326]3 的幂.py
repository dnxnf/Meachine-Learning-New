# 给定一个整数，写一个函数来判断它是否是 3 的幂次方。如果是，返回 true ；否则，返回 false 。 
# 
#  整数 n 是 3 的幂次方需满足：存在整数 x 使得 n == 3ˣ 
# 
#  
# 
#  示例 1： 
# 
#  
# 输入：n = 27
# 输出：true
#  
# 
#  示例 2： 
# 
#  
# 输入：n = 0
# 输出：false
#  
# 
#  示例 3： 
# 
#  
# 输入：n = 9
# 输出：true
#  
# 
#  示例 4： 
# 
#  
# 输入：n = 45
# 输出：false
#  
# 
#  
# 
#  提示： 
# 
#  
#  -2³¹ <= n <= 2³¹ - 1 
#  
# 
#  
# 
#  进阶：你能不使用循环或者递归来完成本题吗？ 
# 
#  Related Topics 递归 数学 👍 362 👎 0

from typing import List, Optional

# leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    def isPowerOfThree(self, n: int) -> bool:
        return n > 0 and 1162261467 % n == 0
# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution)