# 给定一个整数数组 nums 和一个整数目标值 target，请你在该数组中找出 和为目标值 target 的那 两个 整数，并返回它们的数组下标。 
# 
#  你可以假设每种输入只会对应一个答案，并且你不能使用两次相同的元素。 
# 
#  你可以按任意顺序返回答案。 
# 
#  
# 
#  示例 1： 
# 
#  
# 输入：nums = [2,7,11,15], target = 9
# 输出：[0,1]
# 解释：因为 nums[0] + nums[1] == 9 ，返回 [0, 1] 。
#  
# 
#  示例 2： 
# 
#  
# 输入：nums = [3,2,4], target = 6
# 输出：[1,2]
#  
# 
#  示例 3： 
# 
#  
# 输入：nums = [3,3], target = 6
# 输出：[0,1]
#  
# 
#  
# 
#  提示： 
# 
#  
#  2 <= nums.length <= 10⁴ 
#  -10⁹ <= nums[i] <= 10⁹ 
#  -10⁹ <= target <= 10⁹ 
#  只会存在一个有效答案 
#  
# 
#  
# 
#  进阶：你可以想出一个时间复杂度小于 O(n²) 的算法吗？ 
# 
#  Related Topics 数组 哈希表 👍 19828 👎 0

from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    def twoSum1(self, nums: List[int], target: int) -> List[int]:
        #         o(n^2)
        n = len(nums)
        res = []
        for i in range(n):
            for j in range(i + 1, n):
                if nums[i] + nums[j] == target:
                    res.append(i)
                    res.append(j)
                    return res

    def twoSum2(self, nums: List[int], target: int) -> List[int]:
        # 字典，但是没有优化
        dic = {}
        # kv，k是值，v是下标
        n = len(nums)
        res = []
        for i in range(n):
            if target - nums[i] in dic.keys():
                res.append(dic[target - nums[i]])
                res.append(i)
                return res
            elif nums[i] not in dic.keys():
                dic[nums[i]] = i

    def twoSum3(self, nums: List[int], target: int) -> List[int]:
        dic = {}
        for i, num in enumerate(nums):
            tep = target - num
            if tep in dic:
                return [dic[tep], i]
            dic[num] = i

    def twoSum(self, nums: List[int], target: int) -> List[int]:
        dic = {}
        for i, num in enumerate(nums):
            tep = target - num
            if tep in dic:
                return [dic[tep], i]
            dic[num] = i


# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution.twoSum([-1000, 1000, -999, 999, 1001, -1001, 2, -1002, 1004, 5, 18, -1000000], 7))
