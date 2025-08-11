# 给定两个整数数组 preorder 和 inorder ，其中 preorder 是二叉树的先序遍历， inorder 是同一棵树的中序遍历，请构造二叉树并
# 返回其根节点。 
# 
#  
# 
#  示例 1: 
#  
#  
# 输入: preorder = [3,9,20,15,7], inorder = [9,3,15,20,7]
# 输出: [3,9,20,null,null,15,7]
#  
# 
#  示例 2: 
# 
#  
# 输入: preorder = [-1], inorder = [-1]
# 输出: [-1]
#  
# 
#  
# 
#  提示: 
# 
#  
#  1 <= preorder.length <= 3000 
#  inorder.length == preorder.length 
#  -3000 <= preorder[i], inorder[i] <= 3000 
#  preorder 和 inorder 均 无重复 元素 
#  inorder 均出现在 preorder 
#  preorder 保证 为二叉树的前序遍历序列 
#  inorder 保证 为二叉树的中序遍历序列 
#  
# 
#  Related Topics 树 数组 哈希表 分治 二叉树 👍 2546 👎 0

from typing import List, Optional


# favour  前中序构建二叉树，第一次见
#  返回是树时候需要把TreeNode这个类注释了，不然报错
# 问题出在LeetCode的序列化器无法正确识别你本地定义的TreeNode 类。
# 在 LeetCode 环境中，TreeNode 类已经被预先定义，
# 而你本地重新定义了一个同名的类，导致序列化时类型不匹配。
# leetcode submit region begin(Prohibit modification and deletion)
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

class Solution:
    def buildTree(self, preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
        # 已经找到根节点，那么就可以把根节点的左右子树分开了
        # 中序里面，根左边为左子树，右边为右子树，可以递归了
        inorder_map = {val: idx for idx, val in enumerate(inorder)}
        def dfs(pre_start, pre_end, in_start, in_end):
            """
            递归构建二叉树的辅助函数
            :param pre_start: 前序遍历数组的起始索引
            :param pre_end: 前序遍历数组的结束索引
            :param in_start: 中序遍历数组的起始索引
            :param in_end: 中序遍历数组的结束索引
            :return: 当前子树的根节点
            """
            # 如果前序遍历的起始索引大于结束索引，说明当前子树为空
            if pre_start > pre_end:
                return None

            # 前序遍历的第一个元素是当前子树的根节点
            root_val = preorder[pre_start]
            root = TreeNode(root_val)

            # 找到根节点在中序遍历中的位置
            root_pos = inorder_map[root_val]

            # 计算左子树的大小（节点数量）
            left_size = root_pos - in_start

            # 递归构建左子树
            # 左子树的前序遍历范围：pre_start + 1 到 pre_start + left_size
            # 左子树的中序遍历范围：in_start 到 root_pos - 1
            root.left = dfs(pre_start + 1, pre_start + left_size, in_start, root_pos - 1)

            # 递归构建右子树
            # 右子树的前序遍历范围：pre_start + left_size + 1 到 pre_end
            # 右子树的中序遍历范围：root_pos + 1 到 in_end
            root.right = dfs(pre_start + left_size + 1, pre_end, root_pos + 1, in_end)

            return root
        node = dfs(0, len(preorder) - 1, 0, len(inorder) - 1)
        # 从整个数组范围开始递归构建整棵树
        return node

# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()

    # print(solution.buildTree(preorder=[3,9,20,15,7], inorder=[9,3,15,20,7]))
