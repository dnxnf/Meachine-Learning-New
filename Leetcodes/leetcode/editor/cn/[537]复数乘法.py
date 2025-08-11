# 复数 可以用字符串表示，遵循 "实部+虚部i" 的形式，并满足下述条件： 
# 
#  
#  实部 是一个整数，取值范围是 [-100, 100] 
#  虚部 也是一个整数，取值范围是 [-100, 100] 
#  i² == -1 
#  
# 
#  给你两个字符串表示的复数 num1 和 num2 ，请你遵循复数表示形式，返回表示它们乘积的字符串。 
# 
#  
# 
#  示例 1： 
# 
#  
# 输入：num1 = "1+1i", num2 = "1+1i"
# 输出："0+2i"
# 解释：(1 + i) * (1 + i) = 1 + i2 + 2 * i = 2i ，你需要将它转换为 0+2i 的形式。
#  
# 
#  示例 2： 
# 
#  
# 输入：num1 = "1+-1i", num2 = "1+-1i"
# 输出："0+-2i"
# 解释：(1 - i) * (1 - i) = 1 + i2 - 2 * i = -2i ，你需要将它转换为 0+-2i 的形式。 
#  
# 
#  
# 
#  提示： 
# 
#  
#  num1 和 num2 都是有效的复数表示。 
#  
# 
#  Related Topics 数学 字符串 模拟 👍 164 👎 0

from typing import List

# leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    def complexNumberMultiply(self, num1: str, num2: str) -> str:
        # 整数实部,找到第一个加号
        n1 = num1[0:num1.find("+")]
        n2 = num2[0:num2.find("+")]
        # 整数部分
        muln = int(n1) * int(n2)
        i1 = num1[num1.find("+") + 1:num1.find("i")]
        i2 = num2[num2.find("+") + 1:num2.find("i")]
        # 虚数部分
        muli = (-int(i1)) * int(i2)
        realn = muln + muli
        imagi = int(i1) * int(n2) + int(n1) * int(i2)
        # 虚数部分
        res = str(realn) + "+" + str(imagi) + "i"
        return res



# leetcode submit region end(Prohibit modification and deletion)


if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution)
    # num1 = ("-100+1i")
    # a = num1.find("+")
    # print(a)
