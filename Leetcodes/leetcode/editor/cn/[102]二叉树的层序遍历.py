# 给你二叉树的根节点 root ，返回其节点值的 层序遍历 。 （即逐层地，从左到右访问所有节点）。 
# 
#  
# 
#  示例 1： 
#  
#  
# 输入：root = [3,9,20,null,null,15,7]
# 输出：[[3],[9,20],[15,7]]
#  
# 
#  示例 2： 
# 
#  
# 输入：root = [1]
# 输出：[[1]]
#  
# 
#  示例 3： 
# 
#  
# 输入：root = []
# 输出：[]
#  
# 
#  
# 
#  提示： 
# 
#  
#  树中节点数目在范围 [0, 2000] 内 
#  -1000 <= Node.val <= 1000 
#  
# 
#  Related Topics 树 广度优先搜索 二叉树 👍 2143 👎 0

from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
# Definition for a binary tree node.
# favour 二叉树层序遍历,bfs,dfs
#  这样的bfs是能获得每层的节点，然后再逐层打印，这样就能获得层序遍历的结果
#  如果不要逐层打印，可以不用那个for循环，直接遍历完所有节点，然后再逐层打印
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def levelOrder1(self, root: TreeNode) -> List[List[int]]:

        def level(node: TreeNode, depth: int):
            # 从头开始，遇到左右就加1
            if not node:
                return
            # treelist的元素个数对应了层数，而depth大于当前层数，说明要新增一层，
            # 用层次来决定要进入的列表层次
            if len(treelist) < depth:
                # 新增一层空列表
                treelist.append([])
                # 当前节点的值加到那个新列表里面
            treelist[depth - 1].append(node.val)
            if node.left:
                level(node.left, depth + 1)
            if node.right:
                level(node.right, depth + 1)

        # 存放最后的结果，len(treelist)表示层数
        treelist = []

        # 下面两行可有可无
        # if not root:
        #     return []
        level(root, 1)
        return treelist

    def levelOrder(self, root: TreeNode) -> List[List[int]]:
        # bfs
        res = []
        # 存放每一层的
        path = []
        q = []
        # depth = 0
        if not root:
            return []
        q.append(root)
        while q:
            # 得维护一个当前的所有节点，不然都会被加到一起
            cur_lever = len(q)  # 当前层的节点数
            for _ in range(cur_lever):
                node = q.pop(0)
                path.append(node.val)
                if node.left:
                    q.append(node.left)
                if node.right:
                    q.append(node.right)
            res.append(path.copy())
            path.clear()
        return res

    def normal_levelOrder(self, root: TreeNode) -> List[int]:
        #        普通层次遍历，不要path记录每层的节点，直接打印
        if not root:
            return []
        res = []
        q = [root]
        while q:
            node = q.pop(0)
            res.append(node.val)
            if node.left:
                q.append(node.left)
            if node.right:
                q.append(node.right)
        return res


# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    root = TreeNode(3, TreeNode(9), TreeNode(20, TreeNode(15), TreeNode(7)))
    # print(solution.levelOrder(root))
    print(solution.normal_levelOrder(root))
