# 某公司每日销售额记于整数数组 sales，请返回所有 连续 一或多天销售额总和的最大值。 
# 
#  要求实现时间复杂度为 O(n) 的算法。 
# 
#  
# 
#  示例 1： 
# 
#  
# 输入：sales = [-2,1,-3,4,-1,2,1,-5,4]
# 输出：6
# 解释：[4,-1,2,1] 此连续四天的销售总额最高，为 6。 
# 
#  示例 2： 
# 
#  
# 输入：sales = [5,4,-1,7,8]
# 输出：23
# 解释：[5,4,-1,7,8] 此连续五天的销售总额最高，为 23。  
# 
#  
# 
#  提示： 
# 
#  
#  1 <= arr.length <= 10^5 
#  -100 <= arr[i] <= 100 
#  
# 
#  注意：本题与主站 53 题相同：https://leetcode-cn.com/problems/maximum-subarray/ 
# 
#  Related Topics 数组 分治 动态规划 👍 753 👎 0

from typing import List, Optional

# leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    def maxSales(self, sales: List[int]) -> int:
        dp = [-100] * len(sales)
        dp[0] = sales[0]
        for i in range(1, len(sales)):
            # 选或不选
            # 前一天的最大值加上今天的销售额，或只选今天的销售额
            #
            dp[i] = max(dp[i-1]+sales[i], sales[i])
        return max(dp)
# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution)