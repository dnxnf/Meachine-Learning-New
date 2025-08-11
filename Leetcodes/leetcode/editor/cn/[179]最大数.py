# 给定一组非负整数 nums，重新排列每个数的顺序（每个数不可拆分）使之组成一个最大的整数。 
# 
#  注意：输出结果可能非常大，所以你需要返回一个字符串而不是整数。 
# 
#  
# 
#  示例 1： 
# 
#  
# 输入：nums = [10,2]
# 输出："210" 
# 
#  示例 2： 
# 
#  
# 输入：nums = [3,30,34,5,9]
# 输出："9534330"
#  
# 
#  
# 
#  提示： 
# 
#  
#  1 <= nums.length <= 100 
#  0 <= nums[i] <= 10⁹ 
#  
# 
#  Related Topics 贪心 数组 字符串 排序 👍 1355 👎 0
from functools import cmp_to_key
from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    def largestNumber(self, nums: List[int]) -> str:
        str_nums = list(map(str, nums))

        # Custom comparator
        def compare(a, b):
            if a + b > b + a:
                return -1
            else:
                return 1

        # Sort the list using the custom comparator
        str_nums.sort(key=cmp_to_key(compare))

        # Join the sorted strings and handle leading zeros
        result = ''.join(str_nums)
        if result[0] == '0':
            return '0'
        return result


# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution)
