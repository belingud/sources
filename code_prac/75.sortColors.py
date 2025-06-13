"""
75.颜色分类

给定一个包含红色、白色和蓝色、共 n 个元素的数组 nums ，原地 对它们进行排序，使得相同颜色的元素相邻，并按照红色、白色、蓝色顺序排列。

我们使用整数 0、 1 和 2 分别表示红色、白色和蓝色。

必须在不使用库内置的 sort 函数的情况下解决这个问题。

示例 1：

输入：nums = [2,0,2,1,1,0]
输出：[0,0,1,1,2,2]
示例 2：

输入：nums = [2,0,1]
输出：[0,1,2]
"""

from typing import List

class Solution:
    def sortColors(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        # n_ks = {0: 0, 1: 0, 2: 0}
        # for i in nums:
        #     n_ks[i] += 1
        # idx = 0
        # for j, n in n_ks.items():
        #     for _ in range(n):
        #         nums[idx] = j
        #         idx += 1
        l = -1
        r = len(nums)
        i = 0
        while i < r:
            if nums[i] == 0:
                nums[l+1], nums[i] = nums[i], nums[l+1]
                l += 1
                i += 1
            elif nums[i] == 2:
                nums[r-1], nums[i] = nums[i], nums[r-1]
                r -= 1
            else:
                i += 1


if __name__ == "__main__":
    s = Solution()
    colors = [2,0,2,1,1,0]
    s.sortColors(colors)
    print(colors)
