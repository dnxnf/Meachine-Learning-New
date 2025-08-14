# 给定一个正整数 n，返回 连续正整数满足所有数字之和为 n 的组数 。 
# 
#  
# 
#  示例 1: 
# 
#  
# 输入: n = 5
# 输出: 2
# 解释: 5 = 2 + 3，共有两组连续整数([5],[2,3])求和后为 5。 
# 
#  示例 2: 
# 
#  
# 输入: n = 9
# 输出: 3
# 解释: 9 = 4 + 5 = 2 + 3 + 4 
# 
#  示例 3: 
# 
#  
# 输入: n = 15
# 输出: 4
# 解释: 15 = 8 + 7 = 4 + 5 + 6 = 1 + 2 + 3 + 4 + 5 
# 
#  
# 
#  提示: 
# 
#  
#  1 <= n <= 10⁹ 
#  
# 
#  Related Topics 数学 枚举 👍 297 👎 0

from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    def consecutiveNumbersSum_wrong(self, n: int) -> int:
        # 采用数学法，等差数列求和,超时
        '''
        :param n:
        :return:
        首项为a，末项为b，长为l=b-a+1，求和为s，公差为1
        (a+b) * l / 2 = s
        '''
        # 根据这个公式，使用滑动窗口
        if n < 3:
            return 1
        count = 1
        left, right = 1, 2
        res = []
        path = []
        while right <= n // 2 + 1:
            if (right - left + 1) * (right + left) // 2 == n:
                count += 1
                path = [left, right]
                res.append(path)
                path = []
                right += 1
                left += 1
            elif (right - left + 1) * (right + left) // 2 < n:
                right += 1
            else:
                left += 1
        print(res)
        return count

    def consecutiveNumbersSum_wrong2(self, n: int) -> int:
        # 还是超时
        if n < 3:
            return 1
        count = 1  # 至少包含 n 本身（如果允许单个数）
        left, right = 1, 2
        current_sum = 3  # 初始窗口 [1,2] 的和

        while left <= n // 2:
            if current_sum == n:
                count += 1
                current_sum -= left
                left += 1
            elif current_sum < n:
                right += 1
                current_sum += right
            else:
                current_sum -= left
                left += 1
        return count

    def consecutiveNumbersSum(self, n: int) -> int:
        count = 0  # 统计满足条件的连续序列的个数
        # 序列长度 k 的最大可能值是 sqrt(2n) + 2（避免浮点误差）
        k_max = int((2 * n) ** 0.5) + 2

        # 遍历所有可能的序列长度 k（从 1 到 k_max）
        for k in range(1, k_max + 1):
            # 检查 2n 是否能被 k 整除（否则 numerator 不是整数）
            if 2 * n % k == 0:
                # 计算分子部分：2n/k - k + 1
                numerator = 2 * n // k - k + 1
                # 分子必须为正且能被 2 整除（因为 a1 = numerator / 2）
                if numerator > 0 and numerator % 2 == 0:
                    a1 = numerator // 2  # 计算首项 a1
                    # 确保 a1 是正整数（序列至少包含一个正数）
                    if a1 > 0:
                        count += 1  # 找到一个有效序列
        return count

    def consecutiveNumbersSum_wrong3(self, n: int) -> int:
        # 超时
        count = 0
        left = 1  # 窗口左边界（初始为1，确保序列都是正整数）
        current_sum = 0  # 当前窗口的和

        for right in range(1, n + 1):  # 窗口右边界（最多到n）
            current_sum += right  # 扩展窗口

            # 如果当前和大于n，缩小窗口
            while current_sum > n and left <= right:
                current_sum -= left
                left += 1

            # 如果当前和等于n，且序列长度 >=1（left <= right）
            if current_sum == n and left <= right:
                count += 1

        return count

#

# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution)
