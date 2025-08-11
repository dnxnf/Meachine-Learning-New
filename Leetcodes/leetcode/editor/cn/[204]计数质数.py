# 给定整数 n ，返回 所有小于非负整数 n 的质数的数量 。 
# 
#  
# 
#  示例 1： 
# 
#  
# 输入：n = 10
# 输出：4
# 解释：小于 10 的质数一共有 4 个, 它们是 2, 3, 5, 7 。
#  
# 
#  示例 2： 
# 
#  
# 输入：n = 0
# 输出：0
#  
# 
#  示例 3： 
# 
#  
# 输入：n = 1
# 输出：0
#  
# 
#  
# 
#  提示： 
# 
#  
#  0 <= n <= 5 * 10⁶ 
#  
# 
#  Related Topics 数组 数学 枚举 数论 👍 1228 👎 0

from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    # 埃拉托斯特尼筛法（Sieve of Eratosthenes）计算小于 n 的质数个数
    # 时间复杂度 O(n log log n)
    # 空间复杂度 O(n)
    # 思想：
    # 1. 先把 2 这个质数去掉，因为它不是质数
    # 2. 然后从 3 开始遍历，如果当前数是质数，则把它的倍数全部标记为非质数
    # 3. 重复步骤 2，直到遍历到 sqrt(n) 结束
    def countPrimes(self, n: int) -> int:
        if n <= 2:
            return 0
        is_prime = [True] * n
        is_prime[0] = is_prime[1] = False
        for i in range(2, int(n ** 0.5) + 1):
            if is_prime[i]:
                for j in range(i * i, n, i):
                    is_prime[j] = False
        return sum(is_prime)

    def countPrimes2(self, n: int) -> int:
        def is_prime(num: int) -> bool:
            if num < 2:
                return False
            for i in range(2, int(num ** 0.5) + 1):
                if num % i == 0:
                    return False
            return True

        count = 0
        for i in range(2, n):
            if is_prime(i):
                count += 1
        return count


# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution.countPrimes(10))
