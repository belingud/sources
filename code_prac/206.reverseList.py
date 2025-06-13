"""
给你单链表的头节点 head ，请你反转链表，并返回反转后的链表。
输入：head = [1,2,3,4,5]
输出：[5,4,3,2,1]
"""
from typing import Optional
# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
    
class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if not head or not head.next:
            return head
        reversed_head = None
        nodes = []
        while head:
            nodes.append(head.val)
            head = head.next
        if not nodes:
            return None
        reversed_head = ListNode(nodes.pop(-1))
        current = reversed_head
        for i in nodes[::-1]:
            current.next = ListNode(i)
            current = current.next
        return reversed_head


def create_linked_list(lst):
    """根据列表创建链表"""
    if not lst:
        return None
    head = ListNode(lst[0])
    current = head
    for num in lst[1:]:
        current.next = ListNode(num)
        current = current.next
    return head

def print_linked_list(head):
    """打印链表"""
    if not head:
        print("Empty List")
        return
    result = []
    while head:
        result.append(str(head.val))
        head = head.next
    print("->".join(result))

if __name__ == "__main__":
    # 测试用例
    test_cases = [
        [1, 2, 3, 4, 5],  # 正常情况
        [],               # 空链表
        [1],              # 单个节点
        [1, 2]            # 两个节点
    ]
    
    solution = Solution()
    
    for i, test in enumerate(test_cases, 1):
        print(f"测试用例 {i}: 原始链表:", end=" ")
        head = create_linked_list(test)
        print_linked_list(head)
        
        reversed_head = solution.reverseList(head)
        print("        反转后链表:", end=" ")
        print_linked_list(reversed_head)
        print("-" * 50)
