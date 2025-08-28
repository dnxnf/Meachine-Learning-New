# 给你一个区间列表，请你删除列表中被其他区间所覆盖的区间。 
# 
#  只有当 c <= a 且 b <= d 时，我们才认为区间 [a,b) 被区间 [c,d) 覆盖。 
# 
#  在完成所有删除操作后，请你返回列表中剩余区间的数目。 
# 
#  
# 
#  示例： 
# 
#  
# 输入：intervals = [[1,4],[3,6],[2,8]]
# 输出：2
# 解释：区间 [3,6] 被区间 [2,8] 覆盖，所以它被删除了。
#  
# 
#  
# 
#  提示： 
# 
#  
#  1 <= intervals.length <= 1000 
#  0 <= intervals[i][0] < intervals[i][1] <= 10^5 
#  对于所有的 i != j：intervals[i] != intervals[j] 
#  
# 
#  Related Topics 数组 排序 👍 124 👎 0

from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    def removeCoveredIntervals1(self, intervals: List[List[int]]) -> int:
        intervals.sort(key=lambda x: (x[0], -x[1]))
        # 先排左端点，再排右端点，这样可以保证先删除右端点小的区间
        print(intervals)
        # 对于每一个，遍历前面所有的
        num = len(intervals)
        flag = [False] * num
        for i in range(num):
            for j in range(i):
                if intervals[i][0] >= intervals[j][0] and intervals[i][1] <= intervals[j][1]:
                    # 区间i被区间j覆盖，删除区间i
                    flag[i] = True
                    break
        # 统计剩余的区间
        count = 0
        print(flag)
        for i in range(num):
            if not flag[i]:
                count += 1
        return count

    def removeCoveredIntervals(self, intervals: List[List[int]]) -> int:
        # 按左端点升序，右端点降序排序
        intervals.sort(key=lambda x: (x[0], -x[1]))

        count = 0
        max_end = -1  # 记录当前最大右端点
        # 因为左端点一定小，所以右端点只要不大于max_end，就不用考虑
        for interval in intervals:
            # 如果当前区间右端点大于max_end，说明没有被覆盖
            if interval[1] > max_end:
                count += 1
                max_end = interval[1]

        return count
# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution.removeCoveredIntervals([[1, 4], [1, 2], [3, 4]]))
