# 给你一个整数数组 nums ，和一个表示限制的整数 limit，请你返回最长连续子数组的长度，该子数组中的任意两个元素之间的绝对差必须小于或者等于 
# limit 。 
# 
#  如果不存在满足条件的子数组，则返回 0 。 
# 
#  
# 
#  示例 1： 
# 
#  输入：nums = [8,2,4,7], limit = 4
# 输出：2 
# 解释：所有子数组如下：
# [8] 最大绝对差 |8-8| = 0 <= 4.
# [8,2] 最大绝对差 |8-2| = 6 > 4. 
# [8,2,4] 最大绝对差 |8-2| = 6 > 4.
# [8,2,4,7] 最大绝对差 |8-2| = 6 > 4.
# [2] 最大绝对差 |2-2| = 0 <= 4.
# [2,4] 最大绝对差 |2-4| = 2 <= 4.
# [2,4,7] 最大绝对差 |2-7| = 5 > 4.
# [4] 最大绝对差 |4-4| = 0 <= 4.
# [4,7] 最大绝对差 |4-7| = 3 <= 4.
# [7] 最大绝对差 |7-7| = 0 <= 4. 
# 因此，满足题意的最长子数组的长度为 2 。
#  
# 
#  示例 2： 
# 
#  输入：nums = [10,1,2,4,7,2], limit = 5
# 输出：4 
# 解释：满足题意的最长子数组是 [2,4,7,2]，其最大绝对差 |2-7| = 5 <= 5 。
#  
# 
#  示例 3： 
# 
#  输入：nums = [4,2,2,2,4,4,2,2], limit = 0
# 输出：3
#  
# 
#  
# 
#  提示： 
# 
#  
#  1 <= nums.length <= 10^5 
#  1 <= nums[i] <= 10^9 
#  0 <= limit <= 10^9 
#  
# 
#  Related Topics 队列 数组 有序集合 滑动窗口 单调队列 堆（优先队列） 👍 432 👎 0
from collections import deque
from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
# favour 滑动窗口，队列
# todo 队列这个没看懂
class Solution:
    def longestSubarray_wrong(self, nums: List[int], limit: int) -> int:
        # 时间复杂度O(n^2)，超时，拼尽全力无法通过
        '''
        维护一个滑动窗口,和最大值maxn，窗口内的任意元素满足绝对差小于等于limit，
        加入新元素不满足时，left右移，然后继续right右移，直到right到队尾
        窗口右边界不断右移，直到窗口内元素的绝对差大于limit，窗口左边界不断右移，
        直到窗口内元素的绝对差小于等于limit，记录窗口的长度，返回最大长度
        '''
        n = len(nums)
        if n == 1:
            return 1

        left, right = 0, 1
        res = -1
        # 记录窗口内最小值和最大值
        if nums[left] <= nums[right]:
            minn, maxn = nums[left], nums[right]
        else:
            minn, maxn = nums[right], nums[left]

        while right < n:
            # 当前是合法的窗口，更新，右移，判断
            if maxn - minn <= limit:
                res = max(res, right - left + 1)
                right += 1
                if right == n:
                    break
                if minn <= nums[right] <= maxn:
                    continue
                elif nums[right] < minn:
                    minn = nums[right]
                else:
                    maxn = nums[right]
            # 如果当前窗口不合法，left左移到合法为止
            elif maxn - minn > limit:
                # 如果左边界本身是最小值并且后面没有一样的最小值，则更新最小值
                if nums[left] == minn and minn not in nums[left + 1:right + 1]:
                    minn = min(nums[left + 1:right + 1])
                # 如果左边界本身是最大值并且后面没有一样的最大值，则更新最大值
                elif nums[left] == maxn and maxn not in nums[left + 1:right + 1]:
                    maxn = max(nums[left + 1:right + 1])
                left += 1
                # 左边界移动后更新最大最小值

        return res

    def longestSubarray(self, nums: List[int], limit: int) -> int:
        # 时间复杂度O(n)，滑动窗口，队列
        n = len(nums)
        if n == 1:
            return 1

        left, right = 0, 1
        res = 1
        # minq：维护当前窗口最小值的索引（单调递增）
        # maxq：维护当前窗口最大值的索引（单调递减）
        minq = deque([0])  # 存储索引，维护最小值
        maxq = deque([0])  # 存储索引，维护最大值

        while right < n:
            # 维护最小值队列
            # 当最小值索引队列非空，并且当前元素小于等于最小值索引队列最后一个元素指向的元素时，
            while minq and nums[right] < nums[minq[-1]]:
                minq.pop()
            minq.append(right)

            # 维护最大值队列
            # 当最大值队列不为空，并且当前元素大于等于最大值队列最后一个元素指向的元素时，
            while maxq and nums[right] > nums[maxq[-1]]:
                maxq.pop()
            maxq.append(right)

            # 检查当前窗口是否合法
            while nums[maxq[0]] - nums[minq[0]] > limit:
                left += 1
                # 移除超出左边界的元素
                while minq[0] < left:
                    minq.popleft()
                while maxq[0] < left:
                    maxq.popleft()

            # 更新结果
            res = max(res, right - left + 1)
            right += 1

        return res



# leetcode submit region end(Prohibit modification and deletion)


if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution.longestSubarray([8, 2, 4, 7], 4))
    print(Solution().longestSubarray([10, 1, 2, 4, 7, 2], 5))
    print(Solution().longestSubarray([4, 2, 2, 2, 4, 4, 2, 2], 0))
