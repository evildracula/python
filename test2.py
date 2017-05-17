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
        self.convertToStack()

    def convertToStack(self):
        self.reader.skipBlank()
        while not self.reader.isEnd():
            if self.reader.peekNext() == ' ':
                self.reader.skipBlank()
            elif self.reader.peekNext() == '(' or self.reader.peekNext() == ')':
                word = self.reader.readNext()
                self.textStack.insert(0, ('condition', word))
            elif self.reader.peekNext() == 'a':
                word = self.reader.readNext()
                self.textStack.insert(0, ('value', word))
            else:
                self.raiseError('Scan error, char not allow', (None, self.reader.currentPosition))

    def raiseError(self, desc, node):
        raise Exception('%s at %s' % (desc, node[1]))

    def parseCondition(self, status):
        status.append('S')
        finished = False
        # prase result
        value = None
        while len(self.textStack) > 0 and not finished:
            node = self.textStack[-1]
            if status[-1] == 'E':
                status.pop()
                finished = True
            elif status[-1] == 'S':
                if node[1] == '(':
                    self.textStack.pop()
                    status.append('(')
                    value = self.parseCondition(status)
                    status[-1] = 'S2'
                elif node[0] == 'value':
                    status[-1] = 'S2'
                    value = node[1]
                    self.textStack.pop()
                else:
                    self.raiseError('invalid', node)
            elif status[-1] == 'S1':
                if node[0] == 'value':
                    status[-1] = 'S2'
                    value = node[1]
                    self.textStack.pop()
                else:
                    self.raiseError('invalid', node)
            elif status[-1] == 'S2':
                if node[1] == ')':
                    self.textStack.pop()
                    if len(status) > 2 and status[-2] == '(':
                        status.pop()
                        status[-1] = 'E'
                else:
                    status[-1] = 'E'
        return value

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

# s = '(a:"a",(b:"b"|x:"x"))|(c:"c"|(d:"d",e:"e"))'
# s = '(a="a",(b="b"|x=":"))|(c="c"|(d="d",e="e"))'
# s = 'a="a",(b="b"|b="c")'
s = 'aa'
p = Parser(s)
print p.parse()
print p.textStack

