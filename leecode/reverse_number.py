"""
给出一个 32 位的有符号整数，你需要将这个整数中每位上的数字进行反转。

示例 1:
输入: 123
输出: 321

示例 2:
输入: -123
输出: -321

示例 3:
输入: 120
输出: 21

注意:
假设我们的环境只能存储得下 32 位的有符号整数，
则其数值范围为 [−231,  231 − 1]。
请根据这个假设，
如果反转后整数溢出那么就返回 0。
"""
import time

start = time.time()


# class Solution:
#     def reverse(self, x: int) -> int:
#         """
#         字符串反转完成证书的反转
#         用pow()内置方法,相比**较快
#         """
#         # edge = pow(2, 31) - 1 if x > 0 else pow(2, 31)
#         if x < 0:
#             x = -1 * x
#             x = int("-" + str(x)[::-1])
#             # if x < edge:
#             # return 0
#         else:
#             x = int(str(x)[::-1])
#             # if x > edge:
#             # return 0
#         if x < -pow(2, 31) or x > pow(2, 31) - 1:
#             return 0
#         return x


class Solution:
    def reverse(self, x: int) -> int:
        """
        用位运算得取值范围,没有加快运行速度?
        """
        y, res = abs(x), 0
        edge = (1 << 31) - 1 if x > 0 else 1 << 31
        while y != 0:
            res = res * 10 + y % 10
            if res > edge:
                return 0
            y //= 10
        return res if x > 0 else -res


s = Solution()
print(s.reverse(1534236469))
# print(s.reverse(123))

print((time.time() - start) * 1000000)
