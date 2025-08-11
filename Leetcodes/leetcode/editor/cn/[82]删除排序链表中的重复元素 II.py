# 给定一个已排序的链表的头 head ， 删除原始链表中所有重复数字的节点，只留下不同的数字 。返回 已排序的链表 。 
# 
#  
# 
#  示例 1： 
#  
#  
# 输入：head = [1,2,3,3,4,4,5]
# 输出：[1,2,5]
#  
# 
#  示例 2： 
#  
#  
# 输入：head = [1,1,1,2,3]
# 输出：[2,3]
#  
# 
#  
# 
#  提示： 
# 
#  
#  链表中节点数目在范围 [0, 300] 内 
#  -100 <= Node.val <= 100 
#  题目数据保证链表已经按升序 排列 
#  
# 
#  Related Topics 链表 双指针 👍 1372 👎 0

from typing import List, Optional


# leetcode submit region begin(Prohibit modification and deletion)
# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def deleteDuplicates(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if not head:
            return None
        dummy = ListNode(0, head)
        cur = dummy
        # 下一个存在且下下一个存在,判断两个一样不
        while cur.next and cur.next.next:
            if cur.next.val == cur.next.next.val:
                # cur.next = cur.next.next.next
                x = cur.next.val
            #     下一个存在并且下一个也为x
                while cur.next and cur.next.val == x:
                    cur.next = cur.next.next
            else: cur = cur.next
        return dummy.next


# leetcode submit region end(Prohibit modification and deletion)

if __name__ == "__main__":
    # 创建Solution实例
    solution = Solution()
    print(solution)
