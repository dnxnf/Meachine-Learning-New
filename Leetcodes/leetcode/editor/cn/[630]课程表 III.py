# 这里有 n 门不同的在线课程，按从 1 到 n 编号。给你一个数组 courses ，其中 courses[i] = [durationi, 
# lastDayi] 表示第 i 门课将会 持续 上 durationi 天课，并且必须在不晚于 lastDayi 的时候完成。 
# 
#  你的学期从第 1 天开始。且不能同时修读两门及两门以上的课程。 
# 
#  返回你最多可以修读的课程数目。 
# 
#  
# 
#  示例 1： 
# 
#  
# 输入：courses = [[100, 200], [200, 1300], [1000, 1250], [2000, 3200]]
# 输出：3
# 解释：
# 这里一共有 4 门课程，但是你最多可以修 3 门：
# 首先，修第 1 门课，耗费 100 天，在第 100 天完成，在第 101 天开始下门课。
# 第二，修第 3 门课，耗费 1000 天，在第 1100 天完成，在第 1101 天开始下门课程。
# 第三，修第 2 门课，耗时 200 天，在第 1300 天完成。
# 第 4 门课现在不能修，因为将会在第 3300 天完成它，这已经超出了关闭日期。 
# 
#  示例 2： 
# 
#  
# 输入：courses = [[1,2]]
# 输出：1
#  
# 
#  示例 3： 
# 
#  
# 输入：courses = [[3,2],[4,3]]
# 输出：0
#  
# 
#  
# 
#  提示: 
# 
#  
#  1 <= courses.length <= 10⁴ 
#  1 <= durationi, lastDayi <= 10⁴ 
#  
# 
#  Related Topics 贪心 数组 排序 堆（优先队列） 👍 640 👎 0
import heapq
from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    def scheduleCourse(self, courses: List[List[int]]) -> int:
        # 按照结束日期排序
        courses.sort(key=lambda x: x[1])
        max_heap = []  # 存储已选课程的持续时间（负值，用于模拟最大堆）
        current_time = 0
        for duration, last_day in courses:
            # 如果当前课程可以直接加入
            if current_time + duration <= last_day:
                current_time += duration
                heapq.heappush(max_heap, -duration)
            elif max_heap and -max_heap[0] > duration:
                # 如果已选课程中有持续时间比当前课程更长的，则替换
                # （因为这样会减少总时间，同时不减少课程数量，并为后续课程留出更多时间）
                longest_duration = -heapq.heappop(max_heap)
                current_time -= longest_duration
                current_time += duration
                heapq.heappush(max_heap, -duration)
        return len(max_heap)


# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution.scheduleCourse([[100, 200], [200, 1300], [1000, 1250], [2000, 3200]]))
    print(solution.scheduleCourse([[5, 5], [2, 6], [4, 6]]))
