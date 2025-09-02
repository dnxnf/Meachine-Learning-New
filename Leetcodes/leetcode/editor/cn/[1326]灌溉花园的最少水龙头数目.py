# 在 x 轴上有一个一维的花园。花园长度为 n，从点 0 开始，到点 n 结束。 
# 
#  花园里总共有 n + 1 个水龙头，分别位于 [0, 1, ..., n] 。 
# 
#  给你一个整数 n 和一个长度为 n + 1 的整数数组 ranges ，其中 ranges[i] （下标从 0 开始）表示：如果打开点 i 处的水龙头，可
# 以灌溉的区域为 [i - ranges[i], i + ranges[i]] 。 
# 
#  请你返回可以灌溉整个花园的 最少水龙头数目 。如果花园始终存在无法灌溉到的地方，请你返回 -1 。 
# 
#  
# 
#  示例 1： 
# 
#  
# 
#  
# 输入：n = 5, ranges = [3,4,1,1,0,0]
# 输出：1
# 解释：
# 点 0 处的水龙头可以灌溉区间 [-3,3]
# 点 1 处的水龙头可以灌溉区间 [-3,5]
# 点 2 处的水龙头可以灌溉区间 [1,3]
# 点 3 处的水龙头可以灌溉区间 [2,4]
# 点 4 处的水龙头可以灌溉区间 [4,4]
# 点 5 处的水龙头可以灌溉区间 [5,5]
# 只需要打开点 1 处的水龙头即可灌溉整个花园 [0,5] 。
#  
# 
#  示例 2： 
# 
#  
# 输入：n = 3, ranges = [0,0,0,0]
# 输出：-1
# 解释：即使打开所有水龙头，你也无法灌溉整个花园。
#  
# 
#  
# 
#  提示： 
# 
#  
#  1 <= n <= 10⁴ 
#  ranges.length == n + 1 
#  0 <= ranges[i] <= 100 
#  
# 
#  Related Topics 贪心 数组 动态规划 👍 284 👎 0

from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    def minTaps0(self, n: int, ranges: List[int]) -> int:
        can_reach = []
        for i, r in enumerate(ranges):
            if r != 0:
                can_reach.append([max(0, i - r), min(n, i + r)])
        # 如果全0，则无法灌溉
        if not can_reach:
            return -1

        # 得到区间，开始合并，如果一个
        can_reach.sort(key=lambda x: x[0])
        print(can_reach)
        if can_reach[0][0] > 0:
            return -1
        # 合并区间
        max_reach = can_reach[0][1]
        # res = 1
        path = can_reach[0]
        # 从第二个区间开始，如果其更大，则保留，然后再看要不要删除之前的区间


    def minTaps(self, n: int, ranges: List[int]) -> int:
        max_reach = [0] * (n + 1) # 记录每个位置能达到的最大位置
        for i in range(len(ranges)):
            left = max(0, i - ranges[i])
            right = min(n, i + ranges[i])
            max_reach[left] = max(max_reach[left], right)
        print(max_reach) # [5,3,4,0,4,5]
        taps = 0
        curr_end = 0
        next_end = 0
        for i in range(n + 1):
            if i > next_end:
                return -1  # 无法覆盖整个花园
            # 第一行：if i > next_end: return -1
            # 含义：如果当前位置i已经超过了已知能到达的最远位置
            # 为什么：说明有无法覆盖的间隙，比如从位置2最多跳到4，但下一个位置是5，中间有缺口
            if i > curr_end:
                taps += 1
                curr_end = next_end

            next_end = max(next_end, max_reach[i])

        return taps


    def minTaps1(self,n, ranges):
        # 创建 max_reach 数组，记录每个起点能到达的最远位置
        max_reach = [0] * (n + 1)

        for i in range(len(ranges)):
            left = max(0, i - ranges[i])
            right = min(n, i + ranges[i])
            # 对于起点 left，记录能到达的最远位置
            max_reach[left] = max(max_reach[left], right)

        # 类似跳跃游戏 II 的贪心策略
        taps = 0
        curr_end = 0
        next_end = 0

        for i in range(n + 1):
            if i > next_end:
                return -1  # 无法覆盖整个花园

            if i > curr_end:
                taps += 1
                curr_end = next_end

            next_end = max(next_end, max_reach[i])

        return taps


# 测试
# print(minTaps(5, [3, 4, 1, 1, 0, 0]))  # 输出 1
# print(minTaps(3, [0, 0, 0, 0]))  # 输出 -1
# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution.minTaps(5, [3, 4, 1, 1, 0, 0]))
