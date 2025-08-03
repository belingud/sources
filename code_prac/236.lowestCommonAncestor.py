"""
给定一个二叉树, 找到该树中两个指定节点的最近公共祖先。

百度百科中最近公共祖先的定义为：“对于有根树 T 的两个节点 p、q，最近公共祖先表示为一个节点 x，满足 x 是 p、q 的祖先且 x 的深度尽可能大（一个节点也可以是它自己的祖先）。”

输入：root = [3,5,1,6,2,0,8,null,null,7,4], p = 5, q = 1
输出：3
解释：节点 5 和节点 1 的最近公共祖先是节点 3 。
"""


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


class Solution:
    def lowestCommonAncestor(self, root: "TreeNode", p: "TreeNode", q: "TreeNode") -> "TreeNode":
        if root is None:
            return None
        # root为p或q，则root为最近公共祖先
        if root == p or root == q:
            return root
        left = self.lowestCommonAncestor(root.left, p, q)
        right = self.lowestCommonAncestor(root.right, p, q)

        # 如果p和q分别在当前节点的两侧，则当前节点是最近公共祖先
        if left is not None and right is not None:
            return root

        # 如果p和q都在一侧，则返回非空的那一侧的结果
        return left if left is not None else right


class SolutionA:

    def lowestCommonAncestor(self, root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
        if root is None:
            return root
        if root == p or root == q:
            return root
        left = self.lowestCommonAncestor(root.left, p, q)
        right = self.lowestCommonAncestor(root.right, p, q)

        if left is not None and right is not None:
            return root

        return left if left else right


if __name__ == "__main__":
    # 构建测试用例的二叉树: [3,5,1,6,2,0,8,null,null,7,4]
    root = TreeNode(3)
    root.left = TreeNode(5)
    root.right = TreeNode(1)
    root.left.left = TreeNode(6)
    root.left.right = TreeNode(2)
    root.right.left = TreeNode(0)
    root.right.right = TreeNode(8)
    root.left.right.left = TreeNode(7)
    root.left.right.right = TreeNode(4)

    # 测试用例1: p=5, q=1, 期望输出: 3
    p1 = root.left  # 5
    q1 = root.right  # 1
    solution = Solution()
    lca1 = solution.lowestCommonAncestor(root, p1, q1)
    print(f"Test case 1 - LCA of {p1.val} and {q1.val} is: {lca1.val if lca1 else 'None'}")

    # 测试用例2: p=5, q=4, 期望输出: 5
    p2 = root.left  # 5
    q2 = root.left.right.right  # 4
    lca2 = solution.lowestCommonAncestor(root, p2, q2)
    print(f"Test case 2 - LCA of {p2.val} and {q2.val} is: {lca2.val if lca2 else 'None'}")

    # 测试用例3: p=6, q=4, 期望输出: 5
    p3 = root.left.left  # 6
    q3 = root.left.right.right  # 4
    lca3 = solution.lowestCommonAncestor(root, p3, q3)
    print(f"Test case 3 - LCA of {p3.val} and {q3.val} is: {lca3.val if lca3 else 'None'}")
