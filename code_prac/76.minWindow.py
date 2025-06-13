"""
76. 最小覆盖子串
给你一个字符串 s 、一个字符串 t 。返回 s 中涵盖 t 所有字符的最小子串。如果 s 中不存在涵盖 t 所有字符的子串，则返回空字符串 "" 。

注意：
对于 t 中重复字符，我们寻找的子字符串中该字符数量必须不少于 t 中该字符数量。
如果 s 中存在这样的子串，我们保证它是唯一的答案。

输入：s = "ADOBECODEBANC", t = "ABC"
输出："BANC"
解释：最小覆盖子串 "BANC" 包含来自字符串 t 的 'A'、'B' 和 'C'。
"""

from collections import defaultdict
from math import inf


class Solution:
    def minWindow(self, s: str, t: str) -> str:
        if len(s) < len(t):
            return ""
        cnt = defaultdict(int)
        for c in t:
            cnt[c] += 1
        left = 0
        res = ""
        lenMin = inf
        less = len(cnt)
        for right, ch in enumerate(s):
            # 1. 右移right，更新字符计数
            cnt[ch] -= 1
            # cnt[s中的字符]初始值为0，减1之后不可能为0。
            if cnt[ch] == 0:  # 所以这一步里等于0的ch只能是t里的元素
                less -= 1
            # 2. 当窗口满足条件时，尝试收缩左边界
            while less == 0:
                if right - left + 1 < lenMin:
                    lenMin = right - left + 1
                    res = s[left : right + 1]
                # 左移left
                x = s[left]
                if cnt[x] == 0:  # 如果移出的是t中的关键字符
                    less += 1
                cnt[s[left]] += 1
                left += 1
        return res

    def minWindowPrint(self, s: str, t: str) -> str:
        if len(s) < len(t):
            return ""

        cnt = defaultdict(int)
        for c in t:
            cnt[c] += 1

        left = 0
        res = ""
        lenMin = inf
        less = len(cnt)  # 还需要满足的字符种类数

        print(f"初始状态: cnt={dict(cnt)}, less={less}\n")

        for right, ch in enumerate(s):
            cnt[ch] -= 1
            if cnt[ch] == 0:
                less -= 1

            print(f"[右移] right={right}, ch={ch}, cnt={dict(cnt)}, less={less}")

            while less == 0:
                print(f"    [满足条件] 当前窗口: s[{left}:{right + 1}] = '{s[left : right + 1]}'")

                if right - left + 1 < lenMin:
                    lenMin = right - left + 1
                    res = s[left : right + 1]
                    print(f"        [更新最小] lenMin={lenMin}, res='{res}'")

                x = s[left]
                if cnt[x] == 0:
                    less += 1
                cnt[x] += 1
                left += 1

                print(f"  [左移] left={left}, 移出字符={x}, cnt={dict(cnt)}, less={less}")

        print(f"\n最终结果: res='{res}'")
        return res


if __name__ == "__main__":
    so = Solution()
    s = "ADOBECODEBAAC"
    t = "AABC"
    r = so.minWindowPrint(s, t)
    print(f"\n输出结果: '{r}'")
