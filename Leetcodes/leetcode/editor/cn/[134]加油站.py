# 在一条环路上有 n 个加油站，其中第 i 个加油站有汽油 gas[i] 升。 
# 
#  你有一辆油箱容量无限的的汽车，从第 i 个加油站开往第 i+1 个加油站需要消耗汽油 cost[i] 升。你从其中的一个加油站出发，开始时油箱为空。 
# 
#  给定两个整数数组 gas 和 cost ，如果你可以按顺序绕环路行驶一周，则返回出发时加油站的编号，否则返回 -1 。如果存在解，则 保证 它是 唯一 的
# 。 
# 
#  
# 
#  示例 1: 
# 
#  
# 输入: gas = [1,2,3,4,5], cost = [3,4,5,1,2]
# 输出: 3
# 解释:
# 从 3 号加油站(索引为 3 处)出发，可获得 4 升汽油。此时油箱有 = 0 + 4 = 4 升汽油
# 开往 4 号加油站，此时油箱有 4 - 1 + 5 = 8 升汽油
# 开往 0 号加油站，此时油箱有 8 - 2 + 1 = 7 升汽油
# 开往 1 号加油站，此时油箱有 7 - 3 + 2 = 6 升汽油
# 开往 2 号加油站，此时油箱有 6 - 4 + 3 = 5 升汽油
# 开往 3 号加油站，你需要消耗 5 升汽油，正好足够你返回到 3 号加油站。
# 因此，3 可为起始索引。 
# 
#  示例 2: 
# 
#  
# 输入: gas = [2,3,4], cost = [3,4,3]
# 输出: -1
# 解释:
# 你不能从 0 号或 1 号加油站出发，因为没有足够的汽油可以让你行驶到下一个加油站。
# 我们从 2 号加油站出发，可以获得 4 升汽油。 此时油箱有 = 0 + 4 = 4 升汽油
# 开往 0 号加油站，此时油箱有 4 - 3 + 2 = 3 升汽油
# 开往 1 号加油站，此时油箱有 3 - 3 + 3 = 3 升汽油
# 你无法返回 2 号加油站，因为返程需要消耗 4 升汽油，但是你的油箱只有 3 升汽油。
# 因此，无论怎样，你都不可能绕环路行驶一周。 
# 
#  
# 
#  提示: 
# 
#  
#  n == gas.length == cost.length 
#  1 <= n <= 10⁵ 
#  0 <= gas[i], cost[i] <= 10⁴ 
#  输入保证答案唯一。 
#  
# 
#  Related Topics 贪心 数组 👍 1879 👎 0

from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    def canCompleteCircuit(self, gas: List[int], cost: List[int]) -> int:
        # 关键思想1：如果总油量不够总消耗，肯定无法完成
        if sum(cost) > sum(gas):
            return -1

        n = len(gas)  # 加油站数量
        start = 0  # 起始加油站索引
        tank = 0  # 当前油箱剩余油量

        for i in range(n):
            # 计算到达当前加油站后的净油量变化
            tank += gas[i] - cost[i]

            # 关键思想2：如果在i站油箱空了，说明之前的起点都不行
            # 从i+1站重新开始尝试
            if tank < 0:
                start = i + 1  # 更新起点为下一站
                tank = 0  # 重置油箱

        # 关键思想3：如果总油量足够，一定能找到唯一解
        return start


# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution)
