"""
3. 无重复字符的最长子串
给定一个字符串 s ，请你找出其中不含有重复字符的 最长 子串 的长度。

输入: s = "abcabcbb"
输出: 3 
解释: 因为无重复字符的最长子串是 "abc"，所以其长度为 3。
"""
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        """
        s = "abcabcbb"
        return 3
        """
        if not s:
            return 0
        start = 0
        length = 1
        for i, c in enumerate(s):
            if i == 0:
                continue
            pre_c_idx = s.find(c, start, i)
            if pre_c_idx >= 0:
                start = pre_c_idx + 1
            length = max(length, i - start + 1)
        return length


def lengthOfLongestSubstring(s: str) -> int:
    if not s:
        return 0
    start = 0
    max_len = 0
    for idx, i in enumerate(s):
        if idx == 0:
            continue
        tmp = s.find(i, start, idx)
        if tmp >= 0:
            start = tmp + 1
        max_len = max(max_len, idx - start + 1)
    return max_len


if __name__ == "__main__":
    s = Solution()
    print(s.lengthOfLongestSubstring("abcabcbb"))
