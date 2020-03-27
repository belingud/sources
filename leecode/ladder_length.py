"""
给定两个单词（beginWord 和 endWord）和一个字典，
找到从 beginWord 到 endWord 的最短转换序列的长度。
转换需遵循如下规则：

每次转换只能改变一个字母。
转换过程中的中间单词必须是字典中的单词。
说明:

如果不存在这样的转换序列，返回 0。
所有单词具有相同的长度。
所有单词只由小写字母组成。
字典中不存在重复的单词。
你可以假设 beginWord 和 endWord 是非空的，且二者不相同。
示例 1:

输入:
beginWord = "hit",
endWord = "cog",
wordList = ["hot","dot","dog","lot","log","cog"]

输出: 5

解释: 一个最短转换序列是 "hit" -> "hot" -> "dot" -> "dog" -> "cog",
     返回它的长度 5。
示例 2:

输入:
beginWord = "hit"
endWord = "cog"
wordList = ["hot","dot","dog","lot","log"]

输出: 0

解释: endWord "cog" 不在字典中，所以无法进行转换。
"""

from typing import List
import string


class Solution:
    def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> int:
        # length = len(wordList)
        search_list = []
        search_list.append(beginWord)
        while not search_list:
            pass

    def in_list(self, word_list, word):
        for i, v in enumerate(word_list):
            if v == word:
                return True
            if i == len(word_list) - 1 and word != v:
                return False

    def can_change(self, word, current):
        can = 0
        for i in range(len(word)):
            if current[i] != word[i]:
                can += 1
        return can == 1


class Tmp:
    def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> int:
        if endWord not in wordList:
            return 0
        length = len(endWord)
        ws = set(wordList)

        head = {beginWord}
        tail = {endWord}
        tmp = list(string.ascii_lowercase)
        res = 1
        while head:
            if len(head) > len(tail):
                head, tail = tail, head

            q = set()
            for cur in head:
                for i in range(length):
                    for j in tmp:
                        word = cur[:i] + j + cur[i + 1 :]
                        if word in tail:
                            return res + 1
                        if word in ws:
                            q.add(word)
                            ws.remove(word)
            head = q
            res += 1

        return 0
