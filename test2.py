import re


class StringReader(object):
    def __init__(self, text):
        self.text = text
        self.maxlength = len(text)
        self.currentPosition = 0

    def isOverLength(self, length):
        return length >= self.maxlength or length < 0

    def isCurrentPositionValid(self):
        return self.isPositionValid(self.currentPosition)

    def isPositionValid(self, p):
        return p >= 0 and p < self.maxlength

    def peek(self, length):
        if not self.isCurrentPositionValid():
            return None
        m = self.currentPosition
        n = m + length
        if self.isOverLength(n):
            return self.text[m:]
        else:
            return self.text[m:n]

    def peekNext(self):
        return self.peek(1)

    def read(self, length):
        if not self.isCurrentPositionValid():
            return None
        m = self.currentPosition
        n = m + length
        if self.isOverLength(n):
            self.currentPosition = -1
            return self.text[m:]
        else:
            self.currentPosition += length
            return self.text[m:n]

    def readNext(self):
        return self.read(1)

    def skipBlank(self):
        if not self.isCurrentPositionValid():
            return
        while self.peekNext() == ' ':
            self.readNext()

    def readStringPatternWord(self, pattern):
        if not self.isCurrentPositionValid():
            return None
        l = self.peekNext()
        if not l:
            return None
        result = ''
        while l and re.compile(pattern).match(l):
            result += self.readNext()
            l = self.peekNext()
        return result

    def readStringVariable(self):
        if not self.isCurrentPositionValid():
            return None
        m = self.currentPosition
        text = self.text[m:]
        v = self.text[m]
        if v == '"' or v == "'":
            try:
                idx = text.index(v, 1)
                n = idx + 1
                self.currentPosition += n
                if not self.isCurrentPositionValid():
                    self.currentPosition = -1
                return text[:n]
            except ValueError, e:
                return None
        else:
            return None

    def isEnd(self):
        return self.currentPosition == -1


class Parser(object):
    def __init__(self, text):
        self.text = text
        self.textStack = []
        self.parseStack = []
        self.reader = StringReader(text)

        self.pair = {
            ')': '('
        }
        self.syntax_definition = {
            'condition': ['[()\|,]'],
            'operator': ['=']
        }
        self.string_definition = {
            'string': ["""["']"""]
        }
        self.variable_definiation = {
            'variable': ["""[A-Za-z0-9_]"""]
        }
        self.convertToStack()

    def checkDefinition(self, table, char):
        # result = None
        for k, v in table.items():
            for p in v:
                if re.compile(p).match(char):
                    return (k, p)
        return (None, None)

    def convertToStack(self):
        self.reader.skipBlank()
        while not self.reader.isEnd():
            if self.reader.peekNext() == ' ':
                self.reader.skipBlank()
            else:
                char = self.reader.peekNext()
                (syntaxDef, pattern) = self.checkDefinition(self.syntax_definition, char)
                if syntaxDef:
                    self.reader.readNext()
                    self.textStack.insert(0, (syntaxDef, char))
                    continue
                (stringDef, pattern) = self.checkDefinition(self.string_definition, char)
                if stringDef:
                    word = self.reader.readStringVariable()
                    self.textStack.insert(0, (stringDef, word))
                    continue
                (varDef, pattern) = self.checkDefinition(self.variable_definiation, char)
                if varDef:
                    word = self.reader.readStringPatternWord(pattern)
                    self.textStack.insert(0, (stringDef, word))
                    continue
                self.raiseError('Scan error, char not allow', (None, self.reader.currentPosition))

    def raiseError(self, desc, node):
        raise Exception('%s at %s' % (desc, node[1]))

    def parsePush(self, node, status, parseFunc, parseEndStatus):
        self.textStack.pop()
        status.append(node[1])
        result = parseFunc(status)
        status[-1] = parseEndStatus
        return result

    def parsePop(self, node, status, parseEndStatus):
        previousChar = self.pair.get(node[1], None)
        if not previousChar:
            return
        if len(status) > 2 and status[-2] == previousChar:
            self.textStack.pop()
            status.pop()
            status[-1] = parseEndStatus
        else:
            self.raiseError('Parse error, mismatch %s' % node[1], node)

    def parseCondition(self, status):
        status.append('S')
        finished = False
        # prase result
        value = None
        type = None
        node = None
        while len(self.textStack) > 0 and status[-1] != 'E':
            node = self.textStack[-1]
            if status[-1] == 'S':
                if node[1] == '(':
                    (type, value) = self.parsePush(node, status, self.parseCondition, 'S1')
                    type = 'value2'
                elif node[0] == 'value':
                    status[-1] = 'S1'
                    value = node[1]
                    type = 'value'
                    self.textStack.pop()
                else:
                    self.raiseError('invalid', node)
            elif status[-1] == 'S1':
                if node[1] == ')':
                    self.parsePop(node, status, 'E')
                else:
                    if len(self.textStack) == 0:
                        status[-1] = 'E'
                    else:
                        self.raiseError('Parse error', node)
        status.pop()
        print 'Parse router: ', status
        return (type, value)

    def parse(self):
        status = []
        return self.parseCondition(status)

    def loop(self, node):
        n, l, r = node[0], node[1], node[2]
        if n == 'and' or n == 'or':
            left = self.loop(l)
            right = self.loop(r)
            if n == 'and':
                return '(%s %s %s)' % (left, ' && ', right)
            else:
                return '(%s %s %s)' % (left, ' || ', right)
        else:
            return '%s %s %s' % (l, n, r)

    def toDict(self, turpleResult, dict):
        n, l, r = turpleResult[0], turpleResult[1], turpleResult[2]
        if n == 'and' or n == 'or':
            self.toDict(l, dict)
            self.toDict(r, dict)
        else:
            opt = {'opt': n, 'low': r}
            f = dict.get(l, None)
            if not f:
                dict[l] = [opt]
            else:
                dict[l].append(opt)
            return


# A ->  a
#  |     |
#  S     S1
#
#   A -> ( A )
#     (             )
#    <---|  a   |--->
#      S   --->  S1      E
#
#
s = 'abc="123"'
p = Parser(s)
# type, value = p.parse()
# print "%s, %s" % (type, value)
print p.textStack
