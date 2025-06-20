"""
给定一个数组 nums，编写一个函数将所有 0 移动到数组的末尾，同时保持非零元素的相对顺序。

请注意 ，必须在不复制数组的情况下原地对数组进行操作。
"""
from typing import List
class Solution:
    def moveZeroes(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        nonzero_count = 0
        for i in nums:
            if i != 0:
                nums[nonzero_count] = i
                nonzero_count += 1
        for i in range(nonzero_count, len(nums)):
            nums[i] = 0


if __name__ == "__main__":
    s = Solution()
    ns = [0,1,0,3,12]
    s.moveZeroes(ns)
    print(ns)
