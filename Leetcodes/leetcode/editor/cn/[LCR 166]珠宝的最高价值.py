# 现有一个记作二维矩阵 frame 的珠宝架，其中 frame[i][j] 为该位置珠宝的价值。拿取珠宝的规则为： 
# 
#  
#  只能从架子的左上角开始拿珠宝 
#  每次可以移动到右侧或下侧的相邻位置 
#  到达珠宝架子的右下角时，停止拿取 
#  
# 
#  注意：珠宝的价值都是大于 0 的。除非这个架子上没有任何珠宝，比如 frame = [[0]]。 
# 
#  
# 
#  示例 1： 
# 
#  
# 输入：frame = [[1,3,1],[1,5,1],[4,2,1]]
# 输出：12
# 解释：路径 1→3→5→2→1 可以拿到最高价值的珠宝 
# 
#  
# 
#  提示： 
# 
#  
#  0 < frame.length <= 200 
#  0 < frame[0].length <= 200 
#  
# 
#  
# 
#  Related Topics 数组 动态规划 矩阵 👍 554 👎 0

from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    def jewelleryValue1(self, frame: List[List[int]]) -> int:
        m, n = len(frame), len(frame[0])
        dp = [[0] * n for _ in range(m)]
        dp[0][0] = frame[0][0]
        for i in range(1, m):
            dp[i][0] = dp[i - 1][0] + frame[i][0]
        for j in range(1, n):
            dp[0][j] = dp[0][j - 1] + frame[0][j]
        for i in range(1, m):
            for j in range(1, n):
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1]) + frame[i][j]
        return dp[m - 1][n - 1]


# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution)
