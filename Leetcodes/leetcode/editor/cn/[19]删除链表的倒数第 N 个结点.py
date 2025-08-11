# 给你一个链表，删除链表的倒数第 n 个结点，并且返回链表的头结点。 
# 
#  
# 
#  示例 1： 
#  
#  
# 输入：head = [1,2,3,4,5], n = 2
# 输出：[1,2,3,5]
#  
# 
#  示例 2： 
# 
#  
# 输入：head = [1], n = 1
# 输出：[]
#  
# 
#  示例 3： 
# 
#  
# 输入：head = [1,2], n = 1
# 输出：[1]
#  
# 
#  
# 
#  提示： 
# 
#  
#  链表中结点的数目为 sz 
#  1 <= sz <= 30 
#  0 <= Node.val <= 100 
#  1 <= n <= sz 
#  
# 
#  
# 
#  进阶：你能尝试使用一趟扫描实现吗？ 
# 
#  Related Topics 链表 双指针 👍 3150 👎 0

from typing import List, Optional

# leetcode submit region begin(Prohibit modification and deletion)
# Definition for singly-linked list.
# class ListNode:
    # def __init__(self, val=0, next=None):
    #     self.val = val
    #     self.next = next
class Solution:
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        fast = slow = head
        for i in range(n):
            fast = fast.next
        # 移动fast到正数第n个节点
        if not fast:
            return head.next
        # 提前移动了m个节点，slow指针指向倒数第m+n个节点
        while fast.next:
            fast = fast.next
            slow = slow.next
        slow.next = slow.next.next
        return head
# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution.removeNthFromEnd(ListNode(1, ListNode(2, ListNode(3, ListNode(4, ListNode(5))))), 2))