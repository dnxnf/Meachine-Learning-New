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
    def largestNumber1(self, nums: List[int]) -> str:
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

    def largestNumber_wrong(self, nums: List[int]) -> str:
        # 用字典记录不同数字的特点，包括当前的位数，当前位数的数字，以及数字的长度
        # 数字大的放前面，数字相同的谁位数小的放前面
        # 最后按照字典的顺序拼接字符串
        # 将数字转为字符串并提取特征
        num_strs = [str(num) for num in nums]
        digit_info = []
        for s in num_strs:
            digit_info.append({
                'str': s,
                'length': len(s),
                'first_digit': int(s[0]),  # 首位数字
                'num_str': s  # 保留字符串形式用于后续比较
            })

        # Step 2: 自定义排序规则
        def sort_key(x):
            # 按首位数字降序，长度升序，最后按字符串字典序降序
            return (-x['first_digit'], x['length'], -int(x['num_str']))

        digit_info.sort(key=sort_key)

        # Step 3: 拼接结果
        result = ''.join([info['str'] for info in digit_info])

        # Step 4: 处理全零情况
        return result if result[0] != '0' else '0'


# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution)
