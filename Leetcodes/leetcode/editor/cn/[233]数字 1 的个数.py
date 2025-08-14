# 给定一个整数 n，计算所有小于等于 n 的非负整数中数字 1 出现的个数。 
# 
#  
# 
#  示例 1： 
# 
#  
# 输入：n = 13
# 输出：6
#  
# 
#  示例 2： 
# 
#  
# 输入：n = 0
# 输出：0
#  
# 
#  
# 
#  提示： 
# 
#  
#  0 <= n <= 10⁹ 
#  
# 
#  Related Topics 递归 数学 动态规划 👍 617 👎 0

from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    def countDigitOne1(self, n: int) -> int:
        # what 超时了
        if n <= 1:
            return 0 if n == 0 else 1
        dp = [0] * (n + 1)
        # dp[i]表示i中有多少个1
        dp[0] = 0
        dp[1] = 1

        # 对每个数都转成str，数一下1的个数
        for i in range(2, n + 1):
            # 先把i转成str
            dp[i] = dp[i - 1]
            num_str = str(i)
            # 然后把str中的1的个数加到dp[i]中
            for j in range(len(num_str)):
                if num_str[j] == '1':
                    dp[i] += 1
        print(dp)
        return dp[n]

    def countDigitOne(self, n: int) -> int:
        count = 0
        i = 1  # 当前位的权重（初始为个位）
        while i <= n:
            # 高位数字、当前位数字、低位数字
            high = n // (i * 10)
            curr = (n // i) % 10
            low = n % i

            if curr == 0:
                count += high * i
            elif curr == 1:
                count += high * i + (low + 1)
            else:
                count += (high + 1) * i
            i *= 10  # 移动到下一位
        return count


# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution.countDigitOne(13))
