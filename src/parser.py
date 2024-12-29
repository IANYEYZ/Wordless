from tokens import *
import util
import lexer as l

def loadAndRunFile(filename, env):
    tokens = l.lex(filename)
    # for i in tokens:
    #     print(i)
    parseProgram(tokens, env)
    # print(res)

class value:
    # If value is a function:
    # val = (tokens, names)
    def __init__(self, typ, val):
        self.typ = typ
        self.val = val
    def getVal(self, envs):
        if self.typ == "var":
            pos = len(envs) - 1
            while pos >= 0:
                if self.val in envs[pos]:
                    return envs[pos][self.val]
                pos -= 1
        else:
            return self.val
    def call(self, vals, env):
        if self.val == "print":
            for i in vals:
                print(i, end='')
            return value("val", None)
        elif self.val == "import":
            loadAndRunFile(vals[0], env)
            return value("val", None)
        else:
            return callCustom(self.getVal(env), vals, env)

def callCustom(val, vals, env):
    # print(val)
    # print(env)
    env1 = [{}]
    #  + [{self.val[1], vals}]
    for pos, i in enumerate(vals):
        env1[0][val[1][pos]] = i
    env1 = env + env1
    # print("env1: ", env1)
    return value("val", parseExpr(val[0], env1).getVal(env1))

def doOP(res1, res2, op, envs):
    if op == (sym, '+'): return value("val", res1.getVal(envs) + res2.getVal(envs))
    if op == (sym, '-'): return value("val", res1.getVal(envs) - res2.getVal(envs))
    if op == (sym, '*'): return value("val", res1.getVal(envs) * res2.getVal(envs))
    if op == (sym, '/'): return value("val", res1.getVal(envs) / res2.getVal(envs))
    if op == (sym, '='):
        pos = len(envs) - 1
        while pos >= 0:
            if res1.val in envs[pos]:
                envs[pos][res1.val] = res2.getVal(envs)
                return value("var", res1.val)
            pos -= 1
        envs[len(envs) - 1][res1.val] = res2.getVal(envs)
        return value("var", res1.val)
    if op == (sym, '=='): return value("val", int(res1.getVal(envs) == res2.getVal(envs)))
    if op == (sym, '>='): return value("val", int(res1.getVal(envs) >= res2.getVal(envs)))
    if op == (sym, '<='): return value("val", int(res1.getVal(envs) <= res2.getVal(envs)))
    if op == (sym, '>'): return value("val", int(res1.getVal(envs) > res2.getVal(envs)))
    if op == (sym, '<'): return value("val", int(res1.getVal(envs) < res2.getVal(envs)))
    if op == (sym, '!='): return value("val", int(res1.getVal(envs) != res2.getVal(envs)))

def priority(op):
    if op == (sym, '='):
        return 16
    elif op == (sym, '+') or op == (sym, '-'):
        return 6
    elif op == (sym, '*') or op == (sym, '/'):
        return 5
    elif op == (sym, '==') or op == (sym, '>=') or op == (sym, '<=') or op == (sym, '>') or op == (sym, '<') \
     or op == (sym, '!='):
        return 9
    else: return -1

def isBlock(tokens: list) -> bool:
    if tokens[0] == (sym, '{') and tokens[len(tokens) - 1] == (sym, '}') and util.matches(tokens):
        return True
    return False
def parseBlock(tokens_:list, envs:list):
    tokens = tokens_.copy()
    tokens = tokens[1:len(tokens) - 1]
    exprs = util.splitListOut(tokens, (sym, ","))
    res = []
    env1 = envs + [{}]
    for i in exprs:
        res.append(parseExpr(i, env1).getVal(env1))
    return value("val", res)

def isNum(tokens):
    if len(tokens) == 1 and tokens[0][0] == num:
        return True
    return False
def parseNum(tokens, envs:list):
    return value("val", tokens[0][1])

def isString(tokens):
    if len(tokens) == 1 and tokens[0][0] == string:
        return True
    return False
def parseString(tokens, envs:list):
    return value("val", tokens[0][1])

def isName(tokens):
    if len(tokens) == 1 and tokens[0][0] == id:
        return True
    return False
def parseName(tokens, envs:list):
    return value("var", tokens[0][1])

def isParamlist(tokens: list):
    if tokens[0] != (sym, '(') or tokens[len(tokens) - 1] != (sym, ')'): return False
    tks = tokens[1:-1]
    for pos, i in enumerate(tks):
        if i[0] == sym:
            if pos % 2 != 1:
                return False
        elif i[0] == 'id':
            if pos % 2 != 0:
                return False
        elif i[0] != sym and i[0] != "id":
            return False
    return True
def parseParamlist(tokens: list):
    tks = tokens[1:-1]
    res = []
    for i in tks:
        if i[0] == 'id':
            res.append(i[1])
    return res

def isFunction(tokens: list):
    if (sym, "|>") in tokens:
        pos = tokens.index((sym, "|>"))
        tks = tokens[:pos]
        return isParamlist(tks)
    return False
def parseFunction(tokens, envs):
    # print("Here!")
    pos = tokens.index((sym, "|>"))
    tks = tokens[:pos]
    return value("function", (tokens[pos + 1:], parseParamlist(tks)))

def isAtom(tokens):
    if isNum(tokens) or isName(tokens) or isFunction(tokens) or isString(tokens):
        return True

def parseAtom(tokens, envs:list):
    if isNum(tokens):
        return parseNum(tokens, envs)
    elif isName(tokens):
        return parseName(tokens, envs)
    elif isString(tokens):
        return parseString(tokens, envs)
    elif isFunction(tokens):
        return parseFunction(tokens, envs)

def isMatching(tokens):
    if tokens[0] == (sym, '[') and tokens[len(tokens) - 1] == (sym, ']') and util.matches(tokens):
        return True
    return False
def parseMatching(tokens_:list, envs:list):
    tokens = tokens_.copy()
    tokens = tokens[1:len(tokens) - 1]
    matches = util.splitListOut(tokens, (sym, ','))
    # print(matches)
    res = []
    for i in matches:
        match2 = util.splitListOut(i, (sym, '->'))
        # print("match2: ", match2)
        res1 = parseExpr(match2[0], envs)
        env1 = envs + [{}]
        if res1.getVal(envs):
            res.append(parseExpr(match2[1], env1).getVal(env1))
    return value("val", res)

def parseSimpleExpr(tokens, envs:list):
    # print(tokens)
    if tokens[0] == (sym, '(') and tokens[len(tokens) - 1] == (sym, ')'):
        return parseExpr(tokens[1:len(tokens) - 1], envs)
    posi = len(tokens)
    mmax = -1
    paranthese = 0
    for pos, i in enumerate(tokens):
        if priority(i) > mmax and paranthese == 0:
            posi = pos
            mmax = priority(i)
        elif i == (sym, '(') or i == (sym, '{') or i == (sym, '['):
            paranthese += 1
        elif i == (sym, ')') or i == (sym, '}') or i == (sym, ']'):
            paranthese -= 1
    if mmax == -1: # it is a CALL
        pos = util.findMatchingParantheseBack(tokens)
        # print("call: ", pos)
        res1 = parseExpr(tokens[:pos], envs)
        if isinstance(res1.getVal(envs), list):
            res2 = parseExpr(tokens[pos:], envs)
            return value("val", res1.getVal(envs)[res2.getVal(envs)])
        else:
            # print("Here!!!")
            res2 = []
            exprs = util.splitListOut(tokens[pos + 1:-1], (sym, ","))
            for i in exprs:
                res2.append(parseExpr(i, envs).getVal(envs))
            return value("val", res1.call(res2, envs).getVal(envs))
    # print(posi)
    res1 = parseExpr(tokens[:posi], envs)
    res2 = parseExpr(tokens[posi + 1:], envs)
    return doOP(res1, res2, tokens[posi], envs)

def parseExpr(tokens, envs:list):
    # print(tokens)
    if isBlock(tokens):
        return parseBlock(tokens, envs)
    elif isMatching(tokens):
        return parseMatching(tokens, envs)
    elif isAtom(tokens):
        return parseAtom(tokens, envs)
    else:
        return parseSimpleExpr(tokens, envs) 
               # Unfortuanately, seems there's no convenient way to recognize simple expr
               # So it'll be fallback

def parseProgram(tokens, env):
    exprs = util.splitList(tokens, (sym, ';'))
    res = []
    envs = env
    envs[0]['endl'] = '\n'
    for i in exprs:
        # print("Now env: ", envs)
        res.append(parseExpr(i, envs).getVal(envs))
    return res