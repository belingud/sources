"""
给定包含'(', ')', '{', '}', '['和']'字符的字符串，判断该字符串是否有效

字符串是否有效：

1、开括号对应同类型的闭括号

2、按开括号顺序匹配闭括号

注意：空字符串有效
"""


def judge(string: str) -> bool:
    m = {"(": -1, ")": 1, "{": -2, "}": 2, "[": -3, "]": 3}
    _tmp = []
    for i in string:
        if len(_tmp) == 0:
            _tmp.append(i)
            continue
        if m[_tmp[-1]] + m[i] == 0:
            _tmp.pop()
        else:
            _tmp.append(i)
    return not bool(_tmp)


if __name__ == "__main__":
    test_str_1 = "{}[({[]})]"
    test_str_2 = "{{}[}]"
    print(judge(test_str_1))
    print(judge(test_str_2))
