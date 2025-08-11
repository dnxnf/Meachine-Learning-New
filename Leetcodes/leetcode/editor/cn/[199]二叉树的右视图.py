# 给定一个二叉树的 根节点 root，想象自己站在它的右侧，按照从顶部到底部的顺序，返回从右侧所能看到的节点值。 
# 
#  
# 
#  示例 1： 
# 
#  
#  输入：root = [1,2,3,null,5,null,4] 
#  
# 
#  输出：[1,3,4] 
# 
#  解释： 
# 
#  
# 
#  示例 2： 
# 
#  
#  输入：root = [1,2,3,4,null,null,null,5] 
#  
# 
#  输出：[1,3,4,5] 
# 
#  解释： 
# 
#  
# 
#  示例 3： 
# 
#  
#  输入：root = [1,null,3] 
#  
# 
#  输出：[1,3] 
# 
#  示例 4： 
# 
#  
#  输入：root = [] 
#  
# 
#  输出：[] 
# 
#  
# 
#  提示: 
# 
#  
#  二叉树的节点个数的范围是 [0,100] 
#  
#  -100 <= Node.val <= 100 
#  
# 
#  Related Topics 树 深度优先搜索 广度优先搜索 二叉树 👍 1214 👎 0

from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

# favour bfs层序遍历，看一下
class Solution:
    def rightSideView(self, root: Optional[TreeNode]) -> List[int]:
        if not root:
            return []
        #         维护每一层，再把每一层的最后节点输出
        res, path, q = [], [], []
        q.append(root)
        while q:
            cur_lever = len(q) #当前层的节点数
            for _ in range(cur_lever):
                node = q.pop(0)
                # path记录的是每一层，q记录整个树
                path.append(node.val)

                if node.left:
                    q.append(node.left)
                if node.right:
                    q.append(node.right)
            res.append(path[-1])
            path.clear()
        return res




# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution)
