"""
给定一个长度为 n 的整数数组 height 。有 n 条垂线，第 i 条线的两个端点是 (i, 0) 和 (i, height[i]) 。

找出其中的两条线，使得它们与 x 轴共同构成的容器可以容纳最多的水。

返回容器可以储存的最大水量。

说明：你不能倾斜容器。
"""
from typing import List

class Solution:
    """
    给定一个长度为 n 的整数数组 height 。有 n 条垂线，第 i 条线的两个端点是 (i, 0) 和 (i, height[i]) 。

    找出其中的两条线，使得它们与 x 轴共同构成的容器可以容纳最多的水。

    返回容器可以储存的最大水量。

    说明：你不能倾斜容器。
    """

    def maxArea(self, height: List[int]) -> int:
        # left, right 两个指针都从两端开始
        left, max_area = 0
        right = len(height) - 1
        # 两个指针的高度小的那个会被忽略，而大的那个会被保留
        while left < right:
            # max_area 在每次循环中都可能被更新
            max_area = max(max_area, (right - left) * min(height[left], height[right]))
            # 如果 left 高度大于 right 高度，right指针向前移动
            if height[left] >= height[right]:
                right -= 1
            # 如果 right 高度大于 left 高度，left指针向后移动
            else:
                left += 1
        # max_area 保存的是容器最大的水量
        return max_area


if __name__ == "__main__":
    s = Solution()
    heights = [1,8,6,2,5,4,8,3,7]
    m = s.maxArea(heights)
    print(m)
