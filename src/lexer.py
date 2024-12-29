from tokens import *

symbols = [
    "(", ")", "{", "}", "[", "]", ",", "->", "|>", ">=", "<=", ">", "<", "=", "+", "-", "*", "/", "==", ";", "!="
] # Just for reference

symSt = ''.join(a[0] for a in symbols)

def isWhiteSpace(ch):
    return ch == ' ' or ch == '\t' or ch == '\n'
def isChar(ch):
    return not (ch in symSt) and not isWhiteSpace(ch)

def whiteSpace(i, code):
    while i < len(code) and isWhiteSpace(code[i]):
        i = i + 1
    return i

def takeSymbol(i, code, tokens):
    if (i + 1 < len(code)) and code[i:i + 2] in symbols:
        # print("Here!")
        # print("Find token symbol!")
        tokens.append((sym, code[i:i + 2]))
        i = i + 2
    elif code[i:i + 1] in symbols:
        # print("Find token symbol!")
        tokens.append((sym, code[i]))
        i = i + 1
    return i

def takeID(i, code, tokens):
    st = i
    while i < len(code) and isChar(code[i]):
        i = i + 1
    tokens.append((id, code[st:i]))
    return i

def takeComment(i, code):
    while i < len(code) and code[i] != '\n':
        i = i + 1
    return i

def takeNumber(i, code, tokens):
    st = i
    while i < len(code) and code[i].isdigit():
        i = i + 1
    tokens.append((num, int(code[st:i])))
    return i

def takeString(i, code, tokens):
    i = i + 1
    st = i
    while i < len(code) and code[i] != '"':
        i = i + 1
    tokens.append((string, code[st:i]))
    return i + 1

def lex_(code):
    tokens = []
    i = 0
    while i < len(code):
        i = whiteSpace(i, code)
        if i == len(code): break
        if code[i] == '~':
            i = takeComment(i, code)
        elif code[i] == '"':
            i = takeString(i, code, tokens)
        elif code[i] in symSt:
            # print("Find token symbol!")
            i = takeSymbol(i, code, tokens)
        elif code[i].isdigit():
            i = takeNumber(i, code, tokens)
        else:
            # print("Find token id!")
            i = takeID(i, code, tokens)
    return tokens

def lex(filename):
    with open(filename, "r", encoding="UTF-8") as f:
        code = f.read()
        return lex_(code)