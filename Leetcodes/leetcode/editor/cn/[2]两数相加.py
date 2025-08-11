# 给你两个 非空 的链表，表示两个非负的整数。它们每位数字都是按照 逆序 的方式存储的，并且每个节点只能存储 一位 数字。 
# 
#  请你将两个数相加，并以相同形式返回一个表示和的链表。 
# 
#  你可以假设除了数字 0 之外，这两个数都不会以 0 开头。 
# 
#  
# 
#  示例 1： 
#  
#  
# 输入：l1 = [2,4,3], l2 = [5,6,4]
# 输出：[7,0,8]
# 解释：342 + 465 = 807.
#  
# 
#  示例 2： 
# 
#  
# 输入：l1 = [0], l2 = [0]
# 输出：[0]
#  
# 
#  示例 3： 
# 
#  
# 输入：l1 = [9,9,9,9,9,9,9], l2 = [9,9,9,9]
# 输出：[8,9,9,9,0,0,0,1]
#  
# 
#  
# 
#  提示： 
# 
#  
#  每个链表中的节点数在范围 [1, 100] 内 
#  0 <= Node.val <= 9 
#  题目数据保证列表表示的数字不含前导零 
#  
# 
#  Related Topics 递归 链表 数学 👍 11310 👎 0

from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next


class Solution:
    # def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
    #     def get_l(l1, l2, carry=0):
    #         l2value = 0 if l2 is None else l2.val
    #         l1value = 0 if l1 is None else l1.val
    #         f_v = l1value + l2value + carry
    #         carry = f_v // 10
    #         f_v = f_v % 10
    #         return carry, ListNode(f_v)
    #
    #     head = f_node = ListNode()
    #     carry = 0
    #     #  可以把进位也列入到循环里
    #     # while l1 is not None or l2 is not None:
    #     while l1 is not None or l2 is not None or carry:
    #         carry, n_node = get_l(l1, l2, carry)
    #         f_node.next = n_node
    #         f_node = f_node.next
    #
    #         l1 = l1.next if l1 else None
    #         l2 = l2.next if l2 else None
    #     # # 会漏最后一个 进位假如溢出了
    #     # if n_value:
    #     #     f_node.next = ListNode(n_value)
    #
    #     return head.next

    # class Solution:
    #     # 题有问题，过了
    #     # def addTwoNumbers(self, l1: ListNode, l2: ListNode) -> ListNode:
    #     #     p = l1
    #     #     q = l2
    #     #     result = ListNode(-1)
    #     #     curr = result
    #     #     carry = 0
    #     #     while (p != None or q != None):
    #     #         x = p.val if p != None else 0
    #     #         y = q.val if q != None else 0
    #     #
    #     #         s = x + y + carry
    #     #         num = int(s % 10)
    #     #         carry = int(s / 10)
    #     #
    #     #         curr.next = ListNode(num)
    #     #         curr = curr.next
    #     #         p = p if p == None else p.next
    #     #         q = q if q == None else q.next
    #     #
    #     #     if carry > 0:
    #         curr.next = ListNode(carry)
    #
    #     return result.next

    def addTwoNumbers1(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        if not l1 and not l2:
            return None

        if not l1:
            return l2

        if not l2:
            return l1

        # 创建两个空列表，用于存储链表中的数字
        num1 = []
        num2 = []

        # 遍历链表 l1，获取数字
        while l1:
            num1.append(str(l1.val))
            l1 = l1.next

        # 遍历链表 l2，获取数字
        while l2:
            num2.append(str(l2.val))
            l2 = l2.next

        # 反转数字字符串并转换为整数
        n1 = int(''.join(num1[::-1])) if num1 else 0
        n2 = int(''.join(num2[::-1])) if num2 else 0

        # 计算和
        sumn = n1 + n2

        # 如果和为0，直接返回一个包含0的链表
        if sumn == 0:
            return ListNode(0)

        # 将和转换为字符串并反转
        sumn_str = str(sumn)[::-1]

        # 创建结果链表
        dummy = ListNode()
        current = dummy
        for ch in sumn_str:
            current.next = ListNode(int(ch))
            current = current.next

        return dummy.next

    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        # 两个sum，两个cnt，同时计数
        cnt1, cnt2 = 1, 1
        sum1, sum2 = 0, 0
        while l1:
            sum1 += l1.val * cnt1
            cnt1 *= 10
            l1 = l1.next
        while l2:
            sum2 += l2.val * cnt2
            cnt2 *= 10
            l2 = l2.next

        # 计算和
        sum_ = sum1 + sum2
        if sum_ == 0:
            return ListNode(0)
        # 创建结果链表
        dummy = ListNode()
        current = dummy
        while sum_ != 0:
            current.next = ListNode(sum_ % 10)
            current = current.next
            sum_ //= 10

        return dummy.next


# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建示例链表 l1 = [2,4,3]
    l1 = ListNode(2)
    l1.next = ListNode(4)
    l1.next.next = ListNode(3)

    # 创建示例链表 l2 = [5,6,4]
    l2 = ListNode(5)
    l2.next = ListNode(6)
    l2.next.next = ListNode(4)

    l1 = ListNode(0)
    l2 = ListNode(0)
    # 创建Solution实例
    solution = Solution()
    result = solution.addTwoNumbers(l1, l2)

    # 打印结果链表
    while result:
        print(result.val, end=" -> " if result.next else "")
        result = result.next
