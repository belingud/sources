"""
42. 接雨水
给定 n 个非负整数表示每个宽度为 1 的柱子的高度图，计算按此排列的柱子，下雨之后能接多少雨水。

输入：height = [0,1,0,2,1,0,1,3,2,1,2,1]
输出：6
解释：上面是由数组 [0,1,0,2,1,0,1,3,2,1,2,1] 表示的高度图，在这种情况下，可以接 6 个单位的雨水（蓝色部分表示雨水）。 
"""
from typing import List


class Solution:
    def trap(self, height: List[int]) -> int:
        # 示例输入 [0,1,0,2,1,0,1,3,2,1,2,1] 和 [4,2,0,3,2,5]
        # 获取输入数组的长度，代表柱子的数量
        n = len(height)
        # 初始化接雨水量为 0
        ans = 0
        # 初始化左指针，指向数组的起始位置
        left = 0
        # 初始化右指针，指向数组的末尾位置
        right = n - 1
        # 初始化左侧的最大高度为 0
        l_max = 0
        # 初始化右侧的最大高度为 0
        r_max = 0
        # 当左指针小于右指针时，继续循环
        while (left < right):
            # 更新左侧的最大高度
            l_max = max(l_max, height[left])
            # 更新右侧的最大高度
            r_max = max(r_max, height[right])
            # 比较左右指针所指柱子的高度
            if height[left] < height[right]:
                # 如果左侧柱子较低，当前位置能接住的雨水量为左侧最大高度减去当前柱子高度
                ans += l_max - height[left]
                # 左指针右移一位
                left += 1
            else:
                # 如果右侧柱子较低或相等，当前位置能接住的雨水量为右侧最大高度减去当前柱子高度
                ans += r_max - height[right]
                # 右指针左移一位
                right -= 1
        # 返回总的接雨水量
        return ans


if __name__ == "__main__":
    s = Solution()
    print(s.trap([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]))
