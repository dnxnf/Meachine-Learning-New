# 有一些球形气球贴在一堵用 XY 平面表示的墙面上。墙面上的气球记录在整数数组 points ，其中points[i] = [xstart, xend] 表示
# 水平直径在 xstart 和 xend之间的气球。你不知道气球的确切 y 坐标。 
# 
#  一支弓箭可以沿着 x 轴从不同点 完全垂直 地射出。在坐标 x 处射出一支箭，若有一个气球的直径的开始和结束坐标为 xstart，xend， 且满足 
# xstart ≤ x ≤ xend，则该气球会被 引爆 。可以射出的弓箭的数量 没有限制 。 弓箭一旦被射出之后，可以无限地前进。 
# 
#  给你一个数组 points ，返回引爆所有气球所必须射出的 最小 弓箭数 。 
# 
#  示例 1： 
# 
#  
# 输入：points = [[10,16],[2,8],[1,6],[7,12]]
# 输出：2
# 解释：气球可以用2支箭来爆破:
# -在x = 6处射出箭，击破气球[2,8]和[1,6]。
# -在x = 11处发射箭，击破气球[10,16]和[7,12]。 
# 
#  示例 2： 
# 
#  
# 输入：points = [[1,2],[3,4],[5,6],[7,8]]
# 输出：4
# 解释：每个气球需要射出一支箭，总共需要4支箭。 
# 
#  示例 3： 
# 
#  
# 输入：points = [[1,2],[2,3],[3,4],[4,5]]
# 输出：2
# 解释：气球可以用2支箭来爆破:
# - 在x = 2处发射箭，击破气球[1,2]和[2,3]。
# - 在x = 4处射出箭，击破气球[3,4]和[4,5]。 
# 
#  
# 
#  
#  
# 
#  提示: 
# 
#  
#  1 <= points.length <= 10⁵ 
#  points[i].length == 2 
#  -2³¹ <= xstart < xend <= 2³¹ - 1 
#  
# 
#  Related Topics 贪心 数组 排序 👍 1114 👎 0

from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    def findMinArrowShots0(self, points: List[List[int]]) -> int:
        # 超时了timeout
        # 将有交集的合并，合并之后的气球记为一个交集，每遇到一个都和前面的合并

        # 每遇到一个气球，与res判断，看能否合并
        points.sort(key=lambda x: x[0])
        res = [points[0]]
        print(points)
        for i, point in enumerate(points[1:]):
            for j, res_point in enumerate(res):
                # 左端点区大的，右端点取小的
                newLeft = max(point[0], res_point[0])
                newRight = min(point[1], res_point[1])
                if newLeft <= newRight:
                    res[j] = [newLeft, newRight]
                    break
            else:
                res.append(point)
        return len(res)

    def findMinArrowShots(self, points: List[List[int]]) -> int:
        # 贪心算法
        points.sort(key=lambda x: x[1])
        print(points)
        res = 1
        end = points[0][1]
        for i in range(1, len(points)):
            if points[i][0] > end:
                res += 1
                end = points[i][1]
        return res

# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution.findMinArrowShots([[10, 16], [2, 8], [1, 6], [7, 12]]))
