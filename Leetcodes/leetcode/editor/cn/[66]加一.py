# 给定一个表示 大整数 的整数数组 digits，其中 digits[i] 是整数的第 i 位数字。这些数字按从左到右，从最高位到最低位排列。这个大整数不包含
# 任何前导 0。 
# 
#  将大整数加 1，并返回结果的数字数组。 
# 
#  
# 
#  示例 1： 
# 
#  
# 输入：digits = [1,2,3]
# 输出：[1,2,4]
# 解释：输入数组表示数字 123。
# 加 1 后得到 123 + 1 = 124。
# 因此，结果应该是 [1,2,4]。
#  
# 
#  示例 2： 
# 
#  
# 输入：digits = [4,3,2,1]
# 输出：[4,3,2,2]
# 解释：输入数组表示数字 4321。
# 加 1 后得到 4321 + 1 = 4322。
# 因此，结果应该是 [4,3,2,2]。
#  
# 
#  示例 3： 
# 
#  
# 输入：digits = [9]
# 输出：[1,0]
# 解释：输入数组表示数字 9。
# 加 1 得到了 9 + 1 = 10。
# 因此，结果应该是 [1,0]。
#  
# 
#  
# 
#  提示： 
# 
#  
#  1 <= digits.length <= 100 
#  0 <= digits[i] <= 9 
#  digits 不包含任何前导 0。 
#  
# 
#  Related Topics 数组 数学 👍 1506 👎 0

from typing import List, Optional

# leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    def plusOne(self, digits: List[int]) -> List[int]:
        # 得到这个数字，加一后在弄成数组返回
        num = int("".join(map(str, digits))) + 1
        return list(map(int, str(num)))
# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution)