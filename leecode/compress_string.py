"""
字符串压缩。利用字符重复出现的次数，编写一种方法，实现基本的字符串压缩功能。
比如，字符串aabcccccaaa会变为a2b1c5a3。
若“压缩”后的字符串没有变短，则返回原先的字符串。
你可以假设字符串中只包含大小写英文字母（a至z）。

示例1:
输入："aabcccccaaa"
输出："a2b1c5a3"

示例2:
输入："abbccd"
输出："abbccd"
解释："abbccd"压缩后为"a1b2c2d1"，比原字符串长度更长。
"""


class Solution:
    def compressString(self, S: str) -> str:
        result = self.count(S)
        return result if len(result) < len(S) else S

    def count(self, value: str) -> str:
        compressed = ""
        start = -1
        value += "&"
        for index, now in enumerate(value[:-1]):
            next_value = value[index + 1]
            if now != next_value:
                compressed += now + str(index - start)
                start = index
        return compressed


def test_string_compress():
    raw = "aaabbbcccddd"
    solution = Solution()
    compressed = solution.compressString(raw)
    assert compressed == "a3b3c3d3"
