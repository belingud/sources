"""
15. 三数之和
给你一个整数数组 nums ，判断是否存在三元组 [nums[i], nums[j], nums[k]] 满足 i != j、i != k 且 j != k ，同时还满足 nums[i] + nums[j] + nums[k] == 0 。
请你返回所有和为 0 且不重复的三元组。

注意：答案中不可以包含重复的三元组。
"""


class Solution:
    def threeSum(self, nums: list[int]) -> list[list[int]]:
        # 将数字统计入字典中(哈希表)
        data = dict()
        for n in nums:
            if n in data:
                data[n] += 1
            else:
                data[n] = 1
        # 得到由小到大的不同数字数组、及0的位置
        keys = sorted(data.keys())
        N = len(keys)
        zeroAt = 0
        while zeroAt < N and keys[zeroAt] < 0:
            zeroAt += 1
        # 单独讨论三个0的情况
        ret = []
        if 0 in data and data[0] > 2:
            ret.append([0, 0, 0])
        # 各取一个负数a和正数b
        for i in range(zeroAt):
            for j in range(zeroAt + (0 in data), N):
                a = keys[i]
                b = keys[j]
                rest = -a - b
                # 剩下的数必须夹在[a,b]之间，避免重复
                if rest == a and data[a] > 1:
                    ret.append([a, a, b])
                elif a < rest < b and rest in data:
                    ret.append([a, rest, b])
                elif rest == b and data[b] > 1:
                    ret.append([a, b, b])
        return ret


if __name__ == "__main__":
    s = Solution()
    print(s.threeSum([-1, 1, 2, -1, -4]))
    # [[-1,-1,2],[-1,0,1]]
    print(s.threeSum([-4, -1, 3, -2, 6, -1, -2, 3, 1, 1, 2, 2]))
