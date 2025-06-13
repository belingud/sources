"""
49. 字母异位词分组

给你一个字符串数组，请你将 字母异位词 组合在一起。可以按任意顺序返回结果列表。

字母异位词 是由重新排列源单词的所有字母得到的一个新单词。

输入: strs = ["eat", "tea", "tan", "ate", "nat", "bat"]
输出: [["bat"],["nat","tan"],["ate","eat","tea"]]
"""

from typing import List
from collections import defaultdict


class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        sorted_strs = ["".join(sorted(s)) for s in strs]
        str_num = {}
        for idx, i in enumerate(sorted_strs):
            if i not in str_num:
                str_num[i] = [idx]
            else:
                str_num[i].append(idx)
        res = []
        for v in str_num.values():
            res.append([strs[i] for i in v])
        return res
    
    def groupAnagramsBy(self, strs: List[str]) -> list[list[str]]:
        # 如果一些质数的乘积相同，那么这些质数一定相同
        alpha = [2,  3,  5,  7,  11, 13, 17, 19, 23,
                 29, 31, 37, 41, 43, 47, 53, 59, 61,
                 67, 71, 73, 79, 83, 89, 97, 101]
        
        # 使用 defaultdict 来存储分组结果
        cnt = defaultdict(list)
        
        for s in strs:
            mul = 1
            for ch in s:
                # 计算质数乘积
                mul *= alpha[ord(ch) - ord('a')]
            # 将字符串添加到对应的分组
            cnt[mul].append(s)
        
        return list(cnt.values())


if __name__ == '__main__':
    s = Solution()
    print(s.groupAnagrams(["eat", "tea", "tan", "ate", "nat", "bat"]))
