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
                idx = text.index(v,1)
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
            elif self.reader.peekNext() == '"' or self.reader.peekNext() == '"':
                word = self.reader.readStringVariable()
                if word:
                    self.textStack.insert(0, ('value', word))
                else:
                    word = self.reader.readStringPatternWord("""[\w"']""")
                    self.textStack.insert(0, ('name', word))
            elif self.reader.peek(2) == '!=' or self.reader.peek(2) == '>=' or self.reader.peek(2) == '<=' or self.reader.peek(2) == '!#':
                word = self.reader.read(2)
                self.textStack.insert(0, ('operator', word))
            elif self.reader.peekNext() == '(' or self.reader.peekNext() == ')' or self.reader.peekNext() == ',' or self.reader.peekNext() == '|':
                word = self.reader.readNext()
                self.textStack.insert(0, ('condition', word))
            elif self.reader.peekNext() == '@' or self.reader.peekNext() == '!' or self.reader.peekNext() == '@' or self.reader.peekNext() == '=':
                word = self.reader.readNext()
                self.textStack.insert(0, ('operator', word))
            else:
                word = self.reader.readStringPatternWord('\w')
                if word:
                    self.textStack.insert(0, ('name', word))
                else:
                    self.raiseError('Scan error', (None, self.reader.currentPosition))

    def raiseError(self, desc, node):
        raise Exception('%s at %s' % (desc, node[1]))

    def parseConditionPair(self, status):
        operator = None
        fieldName = None
        value = None
        status.append('S')
        finished = False
        while len(self.textStack) > 0 and not finished:
            node = self.textStack[-1]
            if status[-1] == 'S':
                if node[0] == 'name':
                    status[-1] = 'S1'
                    fieldName = node[1]
                    self.textStack.pop()
                else:
                    self.raiseError('Parse error, should be name', node)
            elif status[-1] == 'S1':
                if node[0] == 'operator':
                    status[-1] = 'S2'
                    operator = node[1]
                    self.textStack.pop()
                else:
                    self.raiseError('Parse error, should be operator', node)
            elif status[-1] == 'S2':
                if node[0] == 'value':
                    value = node[1]
                    finished = True
                    self.textStack.pop()
                    status.pop()
                else:
                    self.raiseError('Parse error, should be value', node)
        return (operator, fieldName, value)

    def parseCondition(self, status):
        status.append('S')
        finished = False
        left_result = None
        right_result = None
        operator = None
        while len(self.textStack) > 0 and not finished:
            node = self.textStack[-1]
            if status[-1] == 'S':
                if node[0] == 'condition' and node[1] == '(':
                    self.textStack.pop()
                    status.append('S1')
                    left_result = self.parseCondition(status)
                    status[-1] = 'S2'
                elif node[0] == 'name':
                    left_result = self.parseConditionPair(status)
                    status[-1] = 'S2'
                else:
                    self.raiseError('Parse error, should be nest condition or condition', node)
            elif status[-1] == 'S2':
                if node[0] == 'condition' and node[1] == '|':
                    status[-1] = 'S3'
                    print 'find or'
                    operator = 'or'
                    self.textStack.pop()
                elif node[0] == 'condition' and node[1] == ',':
                    status[-1] = 'S3'
                    print 'find and'
                    operator = 'and'
                    self.textStack.pop()
                elif node[0] == 'condition' and node[1] == ')':
                    self.textStack.pop()
                    status.pop()
                    if status[-1] == 'S1':
                        self.textStack.pop()
                else:
                    self.raiseError('Parse error, should be and or', node)
            elif status[-1] == 'S3':
                if node[0] == 'condition' and node[1] == '(':
                    self.textStack.pop()
                    status.append('S1')
                    right_result = self.parseCondition(status)
                    status[-1] = 'S4'
                elif node[0] == 'name':
                    right_result = self.parseConditionPair(status)
                    status[-1] = 'S4'
                else:
                    self.raiseError('Parse error, should be nest condition or condition', node)
            elif status[-1] == 'S4':
                if node[0] == 'condition' and node[1] == ')':
                    if status[-2] == 'S1':
                        status.pop()
                        status.pop()
                        self.textStack.pop()
                        finished = True
                    else:
                        self.raiseError('Parse error, not allow', node)
                elif node[0] == 'condition':
                    if len(status) > 0:
                        status[-1] = 'S2'
                        left_result = (operator, left_result, right_result)
                else:
                    self.raiseError('Parse error, not be any text here', node)
        if status[-1] in ['S2','S4','S5']:
            status.pop()
        if operator:
            return (operator, left_result, right_result)
        else:
            return left_result

    def parse(self):
        print "stack: <<<%s>>>" % self.textStack
        result = None
        finished = False
        status = []
        result = self.parseCondition(status)
        print status
        print result
        return result


# s = '(a:"a",(b:"b"|x:"x"))|(c:"c"|(d:"d",e:"e"))'
s = '(a="a",(b="b"|x=":"))|(c="c"|(d="d",e="e"))'
p = Parser(s)
# print p.textStack
p.parse()