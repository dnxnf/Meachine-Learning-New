# 小扣打算给自己的 **VS code** 安装使用插件，初始状态下带宽每分钟可以完成 `1` 个插件的下载。假定每分钟选择以下两种策略之一:
# - 使用当前带宽下载插件
# - 将带宽加倍（下载插件数量随之加倍）
# 
# 请返回小扣完成下载 `n` 个插件最少需要多少分钟。
# 
# 注意：实际的下载的插件数量可以超过 `n` 个
# 
# **示例 1：**
# 
# > 输入：`n = 2`
# >
# > 输出：`2`
# >
# > 解释：
# > 以下两个方案，都能实现 2 分钟内下载 2 个插件
# > - 方案一：第一分钟带宽加倍，带宽可每分钟下载 2 个插件；第二分钟下载 2 个插件
# > - 方案二：第一分钟下载 1 个插件，第二分钟下载 1 个插件
# 
# **示例 2：**
# 
# > 输入：`n = 4`
# >
# > 输出：`3`
# >
# > 解释：
# > 最少需要 3 分钟可完成 4 个插件的下载，以下是其中一种方案:
# > 第一分钟带宽加倍，带宽可每分钟下载 2 个插件;
# > 第二分钟下载 2 个插件;
# > 第三分钟下载 2 个插件。
# 
# **提示：**
# - `1 <= n <= 10^5`
# 
#  Related Topics 贪心 数学 动态规划 👍 53 👎 0

from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    def leastMinutes1(self, n: int) -> int:
        if n == 1:
            return 1
        if n == 2:
            return 2
        if n == 3:
            return 3
        if n == 4:
            return 3
        res = 1
        ans = 0
        # 能翻倍就一直翻倍，直到翻倍后大于等于n
        while res < n:
            res *= 2
            ans += 1
        return ans + 1
        # 能下载n个就下载n个，否则下载res个

    def leastMinutes(self, n: int) -> int:
        if n == 1:
            return 1
        if n == 2:
            return 2
        if n == 3:
            return 3
        if n == 4:
            return 3
        # 动态规划,后面的由前面决定，如果前面能下载i个，那么后面就能下载2i个
        dp = [0] * (n + 1)
        dp[1] = 1
        dp[2] = 2
        dp[3] = 3
        dp[4] = 3
        # 如果
        for i in range(5, n + 1):
            dp[i] = min(dp[i - 1] + 1, dp[(i + 1) // 2] + 1)
        return dp[n]


# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution.leastMinutes(8))
