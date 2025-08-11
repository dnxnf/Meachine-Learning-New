# 找出所有相加之和为 n 的 k 个数的组合，且满足下列条件： 
# 
#  
#  只使用数字1到9 
#  每个数字 最多使用一次 
#  
# 
#  返回 所有可能的有效组合的列表 。该列表不能包含相同的组合两次，组合可以以任何顺序返回。 
# 
#  
# 
#  示例 1: 
# 
#  
# 输入: k = 3, n = 7
# 输出: [[1,2,4]]
# 解释:
# 1 + 2 + 4 = 7
# 没有其他符合的组合了。 
# 
#  示例 2: 
# 
#  
# 输入: k = 3, n = 9
# 输出: [[1,2,6], [1,3,5], [2,3,4]]
# 解释:
# 1 + 2 + 6 = 9
# 1 + 3 + 5 = 9
# 2 + 3 + 4 = 9
# 没有其他符合的组合了。 
# 
#  示例 3: 
# 
#  
# 输入: k = 4, n = 1
# 输出: []
# 解释: 不存在有效的组合。
# 在[1,9]范围内使用4个不同的数字，我们可以得到的最小和是1+2+3+4 = 10，因为10 > 1，没有有效的组合。
#  
# 
#  
# 
#  提示: 
# 
#  
#  2 <= k <= 9 
#  1 <= n <= 60 
#  
# 
#  Related Topics 数组 回溯 👍 941 👎 0

from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
# favour 这道题居然是我写出来的，值得纪念一下，用了回溯法
class Solution:
    def combinationSum31(self, k: int, n: int) -> List[List[int]]:
        # 最小值
        mixn = 0
        for i in range(k):
            mixn += (i + 1)
        if mixn > n:
            return []
        # 最大可选数字
        maxn = n
        for i in range(k - 1):
            maxn -= (i + 1)
        # 从最大的开始选，然后减少最大值，直到最大值和次大值差1
        res = []
        path = []

        def backtrack(remain, sumn, maxn, visited):
            # 返回的条件是remain为0，并且path的长度为k
            # remain 记载的是距离目标值的差值,对于每个path得有一个visiter记录，存过的就不存了
            # sumn是当前的和，maxn是当前的最大值，visited是当前的visiter
            #  返回条件
            if remain == 0 and len(path) == k:
                res.append(path.copy()[::-1])
                return
            # 找的过程，从上往下找，找到了就不找了
            for i in range(maxn, 0, -1):
                if i > 9:
                    continue
                if visited[i]:
                    continue
                if sumn + i > n:
                    continue
                if remain - i < 0:
                    continue
                #  如果加进去不会大，没选过，并且
                path.append(i)
                visited[i] = True
                backtrack(remain - i, sumn + i, i - 1, visited)
                path.pop()
                visited[i] = False

        backtrack(n, 0, maxn, [False] * 10)
        return res
    def combinationSum3(self, k: int, n: int) -> List[List[int]]:
        #         上面有点复杂，下面这个正常
        # 计算最小可能和：1+2+...+k
        min_sum = sum(range(1, k + 1))
        # 如果n比最小可能和还小，直接返回空列表
        if min_sum > n:
            return []

        res = []  # 存储最终结果
        path = []  # 存储当前路径/组合

        def backtrack(remain, start, visited):
            """
            回溯函数
            :param remain: 剩余需要凑的和
            :param start: 当前可以开始选择的数字
            :param visited: 记录哪些数字已经被使用过
            """
            # 终止条件：找到k个数字且和为n
            if len(path) == k and remain == 0:
                res.append(path.copy())
                return

            # 从start开始向下选择数字（避免重复组合）
            for num in range(start, 10):  # 数字范围1-9
                # 剪枝条件：
                # 1. 数字已被使用
                # 2. 当前数字太大，会导致remain为负
                if visited[num] or num > remain:
                    continue

                # 选择当前数字
                path.append(num)
                visited[num] = True

                # 递归搜索：remain减少，start从num+1开始（避免重复）
                backtrack(remain - num, num + 1, visited)

                # 撤销选择（回溯）
                path.pop()
                visited[num] = False


        # 初始化visited数组（索引0不使用）
        visited = [False] * 10
        backtrack(n, 1, visited)
        return res

#


# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution.combinationSum3(3, 18))
