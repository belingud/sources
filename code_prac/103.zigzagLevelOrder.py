"""
给你二叉树的根节点 root ，返回其节点值的 锯齿形层序遍历 。（即先从左往右，再从右往左进行下一层遍历，以此类推，层与层之间交替进行）。

输入：root = [3,9,20,null,null,15,7]
输出：[[3],[20,9],[15,7]]

"""

from typing import Optional, List


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def zigzagLevelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        if not root:
            return []
        q = [[root]]
        ans = [[root.val]]
        i = 0
        while q:
            vals = []
            t_ns = []
            ns = q.pop(0)
            for n in ns:
                if n.left:
                    vals.append(n.left.val)
                    t_ns.append(n.left)
                if n.right:
                    vals.append(n.right.val)
                    t_ns.append(n.right)
            if vals:
                ans.append(vals if i % 2 else vals[::-1])
            if t_ns:
                q.append(t_ns)
            i += 1
        return ans


def build_tree(nodes):
    """根据层序遍历的列表构建二叉树"""
    if not nodes:
        return None
    root = TreeNode(nodes[0])
    queue = [root]
    i = 1
    while queue and i < len(nodes):
        node = queue.pop(0)
        if nodes[i] is not None:
            node.left = TreeNode(nodes[i])
            queue.append(node.left)
        i += 1
        if i < len(nodes) and nodes[i] is not None:
            node.right = TreeNode(nodes[i])
            queue.append(node.right)
        i += 1
    return root


if __name__ == "__main__":
    # 测试用例
    test_cases = [
        [3, 9, 20, None, None, 15, 7],  # 标准测试用例
        [1],  # 只有一个节点
        [],  # 空树
        [1, 2, 3, 4, 5, 6, 7],  # 完全二叉树
        [1, None, 2, None, None, 3, 4],  # 只有右子树的树
        [1, 2, None, 3, None, 4, None],  # 只有左子树的树
        [1, 2, 3, 4, None, None, 5],
    ]

    s = Solution()
    for i, test in enumerate(test_cases):
        print(f"测试用例 {i + 1}:")
        print(f"输入: {test}")
        tree = build_tree(test)
        result = s.zigzagLevelOrder(tree) if tree else []
        print(f"输出: {result}")
        print("-" * 50)
