import itertools
from tokens import *

def splitList(l:list, seperator) -> list:
    return [
        list(group) for key, group in itertools.groupby(l, lambda x: x != seperator) if key
    ]

def splitListOut(lst, separator):
    result = []
    current_list = []
    para = 0
    for item in lst:
        if item == (sym, "(") or item == (sym, "[") or item == (sym, "{"):
            para = para + 1
        if item == (sym, ")") or item == (sym, "]") or item == (sym, "}"):
            para = para - 1
        if item == separator and para == 0:
            if current_list:
                result.append(current_list)
            current_list = []
        else:
            current_list.append(item)
    if current_list:
        result.append(current_list)
    return result

def findEither(list1: list, find: list) -> int:
    for pos, i in enumerate(list1):
        if i in find:
            return pos

def findMatchingParantheseBack(list1: list) -> int:
    paranthese = 0
    pos = len(list1) - 1
    while pos >= 0:
        if list1[pos] == (sym, ')') or list1[pos] == (sym, '}') or list1[pos] == (sym, ']'):
            paranthese += 1
        elif list1[pos] == (sym, '(') or list1[pos] == (sym, '{') or list1[pos] == (sym, '['):
            paranthese -= 1
        if paranthese == 0:
            return pos
        pos -= 1

def matches(list1: list) -> bool:
    parathese = 0
    for i in list1[:-1]:
        if i == (sym, ')') or i == (sym, '}') or i == (sym, ']'):
            parathese -= 1
        elif i == (sym, '(') or i == (sym, '{') or i == (sym, '['):
            parathese += 1
        if parathese == 0: return False
    return True