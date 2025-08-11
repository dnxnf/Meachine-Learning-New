# 给定一个 m x n 二维字符网格 board 和一个字符串单词 word 。如果 word 存在于网格中，返回 true ；否则，返回 false 。 
# 
#  单词必须按照字母顺序，通过相邻的单元格内的字母构成，其中“相邻”单元格是那些水平相邻或垂直相邻的单元格。同一个单元格内的字母不允许被重复使用。 
# 
#  
# 
#  示例 1： 
#  
#  
# 输入：board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], word = 
# "ABCCED"
# 输出：true
#  
# 
#  示例 2： 
#  
#  
# 输入：board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], word = 
# "SEE"
# 输出：true
#  
# 
#  示例 3： 
#  
#  
# 输入：board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], word = 
# "ABCB"
# 输出：false
#  
# 
#  
# 
#  提示： 
# 
#  
#  m == board.length 
#  n = board[i].length 
#  1 <= m, n <= 6 
#  1 <= word.length <= 15 
#  board 和 word 仅由大小写英文字母组成 
#  
# 
#  
# 
#  进阶：你可以使用搜索剪枝的技术来优化解决方案，使其在 board 更大的情况下可以更快解决问题？ 
# 
#  Related Topics 深度优先搜索 数组 字符串 回溯 矩阵 👍 2015 👎 0

from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    def exist(self, board: List[List[str]], word: str) -> bool:
        m, n = len(board), len(board[0])
        visited = set()
        res = False

        def dfs(board, i, j, k, visited):
            nonlocal res
            if i >= m or i < 0 or j >= n or j < 0 or (i, j) in visited or board[i][j] != word[k]:
                return
            # k是目标当前的字符的索引
            if k == len(word) - 1:
                res = True
                return
            visited.add((i, j))
            # 向四个方向搜索
            dfs(board, i + 1, j, k + 1, visited)
            dfs(board, i - 1, j, k + 1, visited)
            dfs(board, i, j + 1, k + 1, visited)
            dfs(board, i, j - 1, k + 1, visited)
            # 回溯，因为当前的可以在之后的搜索中使用，所以需要回溯
            visited.remove((i, j))

        for i in range(m):
            for j in range(n):
                if board[i][j] == word[0]:
                    dfs(board, i, j, 0, visited)
        return res


# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    board = [["C", "A", "A"], ["A", "A", "A"], ["B", "C", "D"]]
    word = "AAB"
    print(solution.exist(board, word))
