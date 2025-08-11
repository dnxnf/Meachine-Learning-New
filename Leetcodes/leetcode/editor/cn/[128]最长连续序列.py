# 给定一个未排序的整数数组 nums ，找出数字连续的最长序列（不要求序列元素在原数组中连续）的长度。 
# 
#  请你设计并实现时间复杂度为 O(n) 的算法解决此问题。 
# 
#  
# 
#  示例 1： 
# 
#  
# 输入：nums = [100,4,200,1,3,2]
# 输出：4
# 解释：最长数字连续序列是 [1, 2, 3, 4]。它的长度为 4。 
# 
#  示例 2： 
# 
#  
# 输入：nums = [0,3,7,2,5,8,4,6,0,1]
# 输出：9
#  
# 
#  示例 3： 
# 
#  
# 输入：nums = [1,0,1,2]
# 输出：3
#  
# 
#  
# 
#  提示： 
# 
#  
#  0 <= nums.length <= 10⁵ 
#  -10⁹ <= nums[i] <= 10⁹ 
#  
# 
#  Related Topics 并查集 数组 哈希表 👍 2545 👎 0

from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    def longestConsecutive1(self, nums: List[int]) -> int:
        if not nums:
            return 0
        nums.sort()
        n = len(nums)
        maxn = 0
        cnt = 1  # 当前长度和目前保存的最大长度
        for i in range(1, n):
            # 跳过重复元素
            if nums[i] == nums[i - 1]:
                continue
            # 计算连续序列长度
            if nums[i] == nums[i - 1] + 1:
                cnt += 1
            else:  # 不连续，就更新最大长度
                maxn = max(maxn, cnt)
                cnt = 1
        return max(maxn, cnt)

    def longestConsecutive(self, nums: List[int]) -> int:
        num_set = set(nums)
        max_length = 0

        for num in num_set:
            # 检查是否是序列的起点
            if num - 1 not in num_set:
                current_num = num
                current_length = 1

                # 扩展序列
                while current_num + 1 in num_set:
                    current_num += 1
                    current_length += 1

                # 更新最大长度
                max_length = max(max_length, current_length)

        return max_length

# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution.longestConsecutive([100, 4, 200, 1, 3, 2]))
