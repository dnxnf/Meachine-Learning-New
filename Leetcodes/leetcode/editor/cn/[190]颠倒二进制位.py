# 颠倒给定的 32 位无符号整数的二进制位。 
# 
#  提示： 
# 
#  
#  请注意，在某些语言（如 Java）中，没有无符号整数类型。在这种情况下，输入和输出都将被指定为有符号整数类型，并且不应影响您的实现，因为无论整数是有符号的
# 还是无符号的，其内部的二进制表示形式都是相同的。 
#  在 Java 中，编译器使用二进制补码记法来表示有符号整数。因此，在 示例 2 中，输入表示有符号整数 -3，输出表示有符号整数 -1073741825。
#  
#  
# 
#  
# 
#  示例 1： 
# 
#  
#  输入：n = 43261596 
#  
# 
#  输出：964176192 
# 
#  解释： 
# 
#  
#  
#  
#  整数 
#  二进制 
#  
#  
#  43261596 
#  00000010100101000001111010011100 
#  
#  
#  964176192 
#  00111001011110000010100101000000 
#  
#  
#  
# 
#  示例 2： 
# 
#  
#  输入：n = 2147483644 
#  
# 
#  输出：1073741822 
# 
#  解释： 
# 
#  
#  
#  
#  整数 
#  二进制 
#  
#  
#  2147483644 
#  01111111111111111111111111111100 
#  
#  
#  1073741822 
#  00111111111111111111111111111110 
#  
#  
#  
# 
#  
# 
#  提示： 
# 
#  
#  0 <= n <= 2³¹ - 2 
#  n 为偶数 
#  
# 
#  
# 
#  进阶: 如果多次调用这个函数，你将如何优化你的算法？ 
# 
#  Related Topics 位运算 分治 👍 742 👎 0

from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    def reverseBits(self, n: int) -> int:
        res = int(bin(n)[2:].zfill(32)[::-1], 2)
        return res


# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution)
