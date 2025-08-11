# 给你一个整数 n ，对于 0 <= i <= n 中的每个 i ，计算其二进制表示中 1 的个数 ，返回一个长度为 n + 1 的数组 ans 作为答案。 
# 
# 
#  
# 
#  
#  
#  示例 1： 
#  
#  
# 
#  
# 输入：n = 2
# 输出：[0,1,1]
# 解释：
# 0 --> 0
# 1 --> 1
# 2 --> 10
#  
# 
#  示例 2： 
# 
#  
# 输入：n = 5
# 输出：[0,1,1,2,1,2]
# 解释：
# 0 --> 0
# 1 --> 1
# 2 --> 10
# 3 --> 11
# 4 --> 100
# 5 --> 101
#  
# 
#  
# 
#  提示： 
# 
#  
#  0 <= n <= 10⁵ 
#  
# 
#  
# 
#  进阶： 
# 
#  
#  很容易就能实现时间复杂度为 O(n log n) 的解决方案，你可以在线性时间复杂度 O(n) 内用一趟扫描解决此问题吗？ 
#  你能不使用任何内置函数解决此问题吗？（如，C++ 中的 __builtin_popcount ） 
#  
# 
#  Related Topics 位运算 动态规划 👍 1381 👎 0

from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    def countBits(self, n: int) -> List[int]:
        #  0,1,1,2,1,2,2,3,1,2,2,3,2,3,3,4,
        lst = [0, 1, 1, 2]
        if 4 > n:
            return lst[:n + 1]
        for i in range(4, n + 1):
            lst.append(lst[i // 2] + i % 2)
        return lst

# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution)
