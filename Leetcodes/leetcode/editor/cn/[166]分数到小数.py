# 给定两个整数，分别表示分数的分子 numerator 和分母 denominator，以 字符串形式返回小数 。 
# 
#  如果小数部分为循环小数，则将循环的部分括在括号内。 
# 
#  如果存在多个答案，只需返回 任意一个 。 
# 
#  对于所有给定的输入，保证 答案字符串的长度小于 10⁴ 。 
# 
#  
# 
#  示例 1： 
# 
#  
# 输入：numerator = 1, denominator = 2
# 输出："0.5"
#  
# 
#  示例 2： 
# 
#  
# 输入：numerator = 2, denominator = 1
# 输出："2"
#  
# 
#  示例 3： 
# 
#  
# 输入：numerator = 4, denominator = 333
# 输出："0.(012)"
#  
# 
#  
# 
#  提示： 
# 
#  
#  -2³¹ <= numerator, denominator <= 2³¹ - 1 
#  denominator != 0 
#  
# 
#  Related Topics 哈希表 数学 字符串 👍 515 👎 0

from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    def fractionToDecimal(self, numerator: int, denominator: int) -> str:
        res = ""
        if numerator == 0:
            return "0"
        if (numerator > 0 > denominator) or (numerator < 0 and denominator > 0):
            res += "-"
        numerator = abs(numerator)
        denominator = abs(denominator)
        res += str(numerator // denominator)
        numerator %= denominator
        if numerator == 0:
            return res
        res += "."
        hashmap = {}
        while numerator != 0:
            if numerator in hashmap:
                index = hashmap[numerator]
                res = res[:index] + "(" + res[index:] + ")"
                return res
            hashmap[numerator] = len(res)
            numerator *= 10
            res += str(numerator // denominator)
            numerator %= denominator
        return res

# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution)
