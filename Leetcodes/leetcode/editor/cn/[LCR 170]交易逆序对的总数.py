# 在股票交易中，如果前一天的股价高于后一天的股价，则可以认为存在一个「交易逆序对」。请设计一个程序，输入一段时间内的股票交易记录 record，返回其中存在的
# 「交易逆序对」总数。
#
#
#
#  示例 1：
#
#
# 输入：record = [9, 7, 5, 4, 6]
# 输出：8
# 解释：交易中的逆序对为 (9, 7), (9, 5), (9, 4), (9, 6), (7, 5), (7, 4), (7, 6), (5, 4)。
#
#
#
#
#  提示：
#
#  0 <= record.length <= 50000
#
#  Related Topics 树状数组 线段树 数组 二分查找 分治 有序集合 归并排序 👍 1140 👎 0
from bisect import bisect
from collections import defaultdict
from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    def reversePairs_wrong(self, record: List[int]) -> int:
        # 暴力，超时
        cnt = 0
        n = len(record)
        # t = [0] * (n + 1)
        for i in range(n):
            for j in range(i + 1, n):
                if record[i] > record[j]:
                    cnt += 1
        return cnt

    def reversePairs_wrong2(self, record: List[int]) -> int:
        # 还是超时
        # 字典
        num_indices = defaultdict(list)
        for idx, num in enumerate(record):
            num_indices[num].append(idx)
        # 然后对于dic的元素，找到小于它的元素的个数，然后累加到cnt中
        unique_nums = sorted(num_indices.keys())
        count = 0

        for i in range(len(record)):
            current_num = record[i]
            # 找到所有比current_num小的数值
            for num in unique_nums:
                if num >= current_num:
                    break
                # 获取该数值的所有位置，并统计在i之后出现的次数
                indices = num_indices[num]
                # 使用二分查找找到第一个大于i的位置
                left = bisect.bisect_right(indices, i)
                count += len(indices) - left

        return count

    def reversePairs(self, record: List[int]) -> int:
        def merge_sort(nums, left, right):
            if left >= right:
                return 0
            mid = (left + right) // 2
            count = merge_sort(nums, left, mid) + merge_sort(nums, mid + 1, right)

            # 统计逆序对
            j = mid + 1
            for i in range(left, mid + 1):
                while j <= right and nums[i] > nums[j]:
                    j += 1
                count += j - (mid + 1)  # 从 mid+1 到 j-1 都满足 nums[i] > nums[j]

            # 合并两个有序数组
            temp = []
            i, j = left, mid + 1
            while i <= mid and j <= right:
                if nums[i] <= nums[j]:
                    temp.append(nums[i])
                    i += 1
                else:
                    temp.append(nums[j])
                    j += 1
            while i <= mid:
                temp.append(nums[i])
                i += 1
            while j <= right:
                temp.append(nums[j])
                j += 1

            # 写回原数组
            for k in range(left, right + 1):
                nums[k] = temp[k - left]

            return count

        if not record:
            return 0
        nums = record.copy()
        return merge_sort(nums, 0, len(nums) - 1)
# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution)
