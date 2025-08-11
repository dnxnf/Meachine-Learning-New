# 数字 n 代表生成括号的对数，请你设计一个函数，用于能够生成所有可能的并且 有效的 括号组合。 
# 
#  
# 
#  示例 1： 
# 
#  
# 输入：n = 3
# 输出：["((()))","(()())","(())()","()(())","()()()"]
#  
# 
#  示例 2： 
# 
#  
# 输入：n = 1
# 输出：["()"]
#  
# 
#  
# 
#  提示： 
# 
#  
#  1 <= n <= 8 
#  
# 
#  Related Topics 字符串 动态规划 回溯 👍 3877 👎 0

from typing import List, Optional

# leetcode submit region begin(Prohibit modification and deletion)
# favour 回溯法，我草居然写对了，
'''
所以回溯法先判断回溯终止的条件，也就是找到了一组解
再就是注意下次递归的条件，对于这道题，每个位置
左括号随时都能加入，右括号只有在左括号的数量大于右括号的数量时才加入

因为字符串是不可变的，每次递归都会生成新的 path，所以不需要显式回溯。
如果是用可变对象（如列表），就需要显式回溯来恢复状态。
'''


class Solution:
    def generateParenthesis1(self, n: int) -> List[str]:
        # 好像有点像上一个的字母组合，先给出一个括号的组合，再看后面的能插入到哪里
        res = []

        # start是位置，从0到2n-1
        # path是当前的组合，remain是还需要的括号数
        def backtrack(start, path: list, remain, numLeft, numRight):
            # 结束条件
            if remain == 0:
                res.append(''.join(path))
                return
            # 剪枝
            if remain < 0 or start > 2 * n - 1:
                return
            # 选择，左括号或者右括号
            # 什么情况下能选左括号，与path栈顶无关，只要左括号总数不超过n就行
            if numLeft < n:  # 0,1,2
                path.append('(')
                backtrack(start + 1, path, remain - 1, numLeft + 1, numRight)
                path.pop()
            # 什么情况下能选右括号，与path栈顶无关，只要右括号数量不超过numLeft就行
            if numRight < numLeft:  # 0,1,2
                path.append(')')
                backtrack(start + 1, path, remain - 1, numLeft, numRight + 1)
                path.pop()

        backtrack(0, [], 2 * n, 0, 0)
        return res

    def generateParenthesis2(self, n: int) -> List[str]:
        # 对上面的优化，减少了多余的参数
        res = []

        def backtrack(path: str, left: int, right: int):
            # 结束条件
            if len(path) == 2 * n:
                res.append(path)
                return
            # 下一次递归的条件
            if left < n:
                backtrack(path + '(', left + 1, right)
            if right < left:
                backtrack(path + ')', left, right + 1)

        # 因为字符串不可变，所以不用显式的回溯，
        # 最后一步返回，path 仍然是 '('，继续 right < left 分支，
        # 调用 backtrack('()', 1, 1),后续递归类似
        backtrack('', 0, 0)
        return res

    def generateParenthesis(self, n: int) -> List[str]:
        # 动态规划，用一个数组来记录每个位置的左右括号的数量
        # 对于每个位置，左括号的数量一定是右括号的数量的上限
        # 所以只需要记录左括号的数量即可

        dp = [[] for _ in range(n + 1)]
        dp[0] = ['']
        # dp[1] = ['()']
        for i in range(1, n + 1):
            for j in range(i):
                for left in dp[j]:
                    for right in dp[i - 1 - j]:
                        dp[i].append("(" + left + ")" + right)
        return dp[n]
# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution.generateParenthesis(2))
