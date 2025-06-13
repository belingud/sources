"""
给你一个整数数组 nums 和一个整数 k ，请你返回其中出现频率前 k 高的元素。你可以按 任意顺序 返回答案。

输入: nums = [1,1,1,2,2,3], k = 2
输出: [1,2]
"""

from typing import List
from collections import Counter


class Solution:
    def topKFrequentA(self, nums: List[int], k: int) -> List[int]:
        c = Counter(nums)
        # return heapq.nlargest(k, c.keys(), key=c.get)
        nums_count = [(k, v) for k, v in c.items()]
        nlargest_tuple = sorted(nums_count, key=lambda x: x[1], reverse=True)[:k]
        return [i[0] for i in nlargest_tuple]

    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        return [i[0] for i in Counter(nums).most_common(k)]


if __name__ == "__main__":
    s = Solution()
    nums = [1, 1, 1, 2, 2, 3]
    k = 2
    r = s.topKFrequent(nums, k)
    print(r)
