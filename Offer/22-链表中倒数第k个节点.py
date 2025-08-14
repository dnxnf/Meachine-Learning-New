'''
题目：链表中倒数第k个节点
输入一个链表，输出该链表中倒数第K的结点，为了符合大多数人的习惯，本题从1开始计数，即链表的尾结点是倒数第1个节点。
例如，一个链表有6个节点，从头节点开始，它们的值依次是1、2、3、4、5、6，这个链表的倒数第3个节点是指为4的节点。
'''


class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


class Solution:
    def removeNthFromEnd2(self, head: ListNode, k: int):
        # write your code here
        if k == 0 or head is None:
            return None
        fast = slow = head
        # 快指针先走k步
        for _ in range(k):
            if not fast:
                return None  # 链表长度不足k
            fast = fast.next
        # 快慢指针同时移动，直到快指针到达末尾
        while fast:
            fast = fast.next
            slow = slow.next
        return slow.val

    def removeNthFromEnd(self, head, n):
        # write your code here
        if n == 0 or head is None:
            return None
        ahead_node = behind_node = head
        for i in range(n - 1):
            if ahead_node.next is not None:
                ahead_node = ahead_node.next
            else:
                return None
        while ahead_node.next is not None:
            ahead_node = ahead_node.next
            behind_node = behind_node.next
        return behind_node

head = ListNode(1)
head.next = ListNode(2)
head.next.next = ListNode(3)
head.next.next.next = ListNode(4)
head.next.next.next.next = ListNode(5)
head.next.next.next.next.next = ListNode(6)
s = Solution()
print(s.removeNthFromEnd2(head, 10))