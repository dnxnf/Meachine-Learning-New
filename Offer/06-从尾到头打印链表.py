'''
题目：
输入一个链表的头节点，从尾到头反过来打印出每个节点的值。
'''


# Definition of ListNode

class ListNode(object):

    def __init__(self, val, next=None):
        self.val = val
        self.next = next


# 递归
def PrintListReversingly(head):
    if head:
        if head.next:
            PrintListReversingly(head.next)
        print(head.val)


# 栈
def PrintListReversingly2(head):
    stack = []
    while head is not None:
        stack.append(head.val)
        head = head.next
    while stack:
        print(stack.pop())
    # print()

if __name__ == '__main__':
    # 创建链表
    head = ListNode(1)
    head.next = ListNode(2)
    head.next.next = ListNode(3)
    head.next.next.next = ListNode(4)
    # head.next.next = ListNode(5)
    PrintListReversingly(head)
    print('-----------')
    PrintListReversingly2(head)

