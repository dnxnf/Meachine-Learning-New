# 给你一个 n x n 矩阵 matrix ，其中每行和每列元素均按升序排序，找到矩阵中第 k 小的元素。 请注意，它是 排序后 的第 k 小元素，而不是第 
# k 个 不同 的元素。 
# 
#  你必须找到一个内存复杂度优于 O(n²) 的解决方案。 
# 
#  
# 
#  示例 1： 
# 
#  
# 输入：matrix = [[1,5,9],[10,11,13],[12,13,15]], k = 8
# 输出：13
# 解释：矩阵中的元素为 [1,5,9,10,11,12,13,13,15]，第 8 小元素是 13
#  
# 
#  示例 2： 
# 
#  
# 输入：matrix = [[-5]], k = 1
# 输出：-5
#  
# 
#  
# 
#  提示： 
# 
#  
#  n == matrix.length 
#  n == matrix[i].length 
#  1 <= n <= 300 
#  -10⁹ <= matrix[i][j] <= 10⁹ 
#  题目数据 保证 matrix 中的所有行和列都按 非递减顺序 排列 
#  1 <= k <= n² 
#  
# 
#  
# 
#  进阶： 
# 
#  
#  你能否用一个恒定的内存(即 O(1) 内存复杂度)来解决这个问题? 
#  你能在 O(n) 的时间复杂度下解决这个问题吗?这个方法对于面试来说可能太超前了，但是你会发现阅读这篇文章（ this paper ）很有趣。 
#  
# 
#  Related Topics 数组 二分查找 矩阵 排序 堆（优先队列） 👍 1135 👎 0
import heapq
import itertools
from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    def kthSmallest(self, matrix: List[List[int]], k: int) -> int:
        m, n = len(matrix), len(matrix[0])
        # 先将矩阵中的元素全部放入一个列表中
        nums = list(itertools.chain(*matrix))
        # 然后使用堆排序算法，找出第 k 小的元素
        heapq.heapify(nums)
        for i in range(k):
            res = heapq.heappop(nums)
        return res


# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution)
