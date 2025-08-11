# 给你一棵二叉树的根节点 root ，返回树的 最大宽度 。 
# 
#  树的 最大宽度 是所有层中最大的 宽度 。 
# 
#  
#  
#  每一层的 宽度 被定义为该层最左和最右的非空节点（即，两个端点）之间的长度。将这个二叉树视作与满二叉树结构相同，两端点间会出现一些延伸到这一层的 
# null 节点，这些 null 节点也计入长度。 
#  
#  
# 
#  题目数据保证答案将会在 32 位 带符号整数范围内。 
# 
#  
# 
#  示例 1： 
#  
#  
# 输入：root = [1,3,2,5,3,null,9]
# 输出：4
# 解释：最大宽度出现在树的第 3 层，宽度为 4 (5,3,null,9) 。
#  
# 
#  示例 2： 
#  
#  
# 输入：root = [1,3,2,5,null,null,9,6,null,7]
# 输出：7
# 解释：最大宽度出现在树的第 4 层，宽度为 7 (6,null,null,null,null,null,7) 。
#  
# 
#  示例 3： 
#  
#  
# 输入：root = [1,3,2,5]
# 输出：2
# 解释：最大宽度出现在树的第 2 层，宽度为 2 (3,2) 。
#  
# 
#  
# 
#  提示： 
# 
#  
#  树中节点的数目范围是 [1, 3000] 
#  -100 <= Node.val <= 100 
#  
# 
#  Related Topics 树 深度优先搜索 广度优先搜索 二叉树 👍 698 👎 0

from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def widthOfBinaryTree(self, root: Optional[TreeNode]) -> int:
        if not root:
            return 0
        # 只记录每层最先访问到的最左节点位置
        # 后续同层节点与最左节点位置差即为当前宽度
        m_left = {}  # 每层最先访问到的节点位置（即最左位置）。
        maxn = 0  # 最大宽度

        def dfs(node, depth, pos):
            nonlocal maxn
            if not node:
                return
            # 当层还没有被记录
            if depth not in m_left:
                # depth是深度key，对应了位置pos
                # 如果是该层第一个访问的节点，记录其位置
                m_left[depth] = pos

            #   每次递归做的事情
            #   当前宽度 = 当前节点位置 - 同层最左位置 + 1
            cur_width = pos - m_left[depth] + 1
            maxn = max(maxn, cur_width)

            # 左右子树需要做什么，记录最左的序号，深度加一
            dfs(node.left, depth + 1, pos * 2 + 1)
            dfs(node.right, depth + 1, pos * 2 + 2)

        dfs(root, 1, 0)
        return maxn


# leetcode submit region end(Prohibit modification and deletion)


if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution)
