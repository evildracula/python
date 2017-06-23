# -*- coding: utf-8 -*-
import urllib.request
import urllib.parse
import json
import hashlib

def sendRequest(url, headers, body):
    # ssl._create_default_https_context = ssl._create_unverified_context
    req = urllib.request.Request(url)
    for k, v in headers.items():
        req.add_header(k, v)
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor)
    try:
        response = opener.open(req, body)
        return (response.code, '', response.read())
    except urllib.request.HTTPError as e:
        return (e.code, e.reason, e.read())
    except urllib.request.URLError as e:
        return (None, e.reason, None)


def getWXToken(appId, secret):
    url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s"
    url = url % (appId, secret)
    headers = {}
    headers['Content-Type'] = 'application/json'
    body = b""
    (code, reason, result) = sendRequest(url, headers, body)
    return json.loads(result.decode('utf-8'))

def getWXJSAPITicket(accessToken):
    url = "https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token=%s&type=jsapi"
    url = url % accessToken
    headers = {}
    headers['Content-Type'] = 'application/json'
    body = b""
    (code, reason, result) = sendRequest(url, headers, body)
    return json.loads(result.decode('utf-8'))

# access_token = getWXToken('wx9f248acc2b1a683b','e26c5dac6f18a94a11cb1bd72ec5b897')['access_token']
# print(access_token)
# jsapiticket = getWXJSAPITicket(access_token)
# print(jsapiticket)

def getSign(noncestr, ticket, timestamp, url):
    parameters = {
        'jsapi_ticket':ticket,
        'noncestr':noncestr,
        'timestamp': timestamp,
        'url':url
    }
    sortedParameters = [(k, parameters[k]) for k in sorted(parameters.keys())]
    parameterString = urllib.parse.urlencode(sortedParameters,safe=':/?=')
    print(parameterString)
    result = hashlib.sha1(parameterString.encode('utf-8'))
    print(result.hexdigest())
    return result.hexdigest()

print(getSign('abcd','bxLdikRXVbTPdHSM05e5uz8bKdXS-R7b7ZkHU3GWADSW5wt_WDZTb-sIiAvPdj1w7voeRs82BVwI8QWyxuc-Yg',1497945805,'http://www.xuxiaoye.com/index'))


# import re
# import yaml
#
#
# class StringReader(object):
#     def __init__(self, text):
#         self.text = text
#         self.maxlength = len(text)
#         self.currentPosition = 0
#
#     def isOverLength(self, length):
#         return length >= self.maxlength or length < 0
#
#     def isCurrentPositionValid(self):
#         return self.isPositionValid(self.currentPosition)
#
#     def isPositionValid(self, p):
#         return p >= 0 and p < self.maxlength
#
#     def peek(self, length):
#         if not self.isCurrentPositionValid():
#             return None
#         m = self.currentPosition
#         n = m + length
#         if self.isOverLength(n):
#             return self.text[m:]
#         else:
#             return self.text[m:n]
#
#     def peekNext(self):
#         return self.peek(1)
#
#     def read(self, length):
#         if not self.isCurrentPositionValid():
#             return None
#         m = self.currentPosition
#         n = m + length
#         if self.isOverLength(n):
#             self.currentPosition = -1
#             return self.text[m:]
#         else:
#             self.currentPosition += length
#             return self.text[m:n]
#
#     def readNext(self):
#         return self.read(1)
#
#     def skipBlank(self):
#         if not self.isCurrentPositionValid():
#             return
#         while self.peekNext() == ' ':
#             self.readNext()
#
#     def readStringPatternWord(self, pattern):
#         if not self.isCurrentPositionValid():
#             return None
#         l = self.peekNext()
#         if not l:
#             return None
#         result = ''
#         while l and re.compile(pattern).match(l):
#             result += self.readNext()
#             l = self.peekNext()
#         return result
#
#     def readStringVariable(self):
#         if not self.isCurrentPositionValid():
#             return None
#         m = self.currentPosition
#         text = self.text[m:]
#         v = self.text[m]
#         if v == '"' or v == "'":
#             try:
#                 idx = text.index(v, 1)
#                 n = idx + 1
#                 self.currentPosition += n
#                 if not self.isCurrentPositionValid():
#                     self.currentPosition = -1
#                 return text[:n]
#             except ValueError, e:
#                 return None
#         else:
#             return None
#
#     def isEnd(self):
#         return self.currentPosition == -1
#
#
# class Parser(object):
#     def __init__(self, text):
#         self.text = text
#         self.textStack = []
#         self.parseStack = []
#         self.priorityStack = []
#         self.reader = StringReader(text)
#         self.pair = {
#             ')': '('
#         }
#
#         self.syntax_definition = {
#             'condition': [
#                 (1, '\('),
#                 (1, '\)'),
#                 (1, '\|'),
#                 (1, ',')
#             ],
#             'operator': [
#                 (1, '='),
#                 (2, '!='),
#                 (1, '@'),
#                 (2, '!@'),
#                 (1, '#'),
#                 (2, '!#'),
#                 (1, '>'),
#                 (1, '<'),
#                 (2, '>='),
#                 (2, '<=')
#             ]
#         }
#         self.string_definition = {
#             'string': [(1, """["']""")]
#         }
#         self.variable_definiation = {
#             'variable': [(1, """[A-Za-z0-9_]""")]
#         }
#         self.convertToStack()
#
#     def checkDefinition(self, table, char):
#         # result = None
#         for k, v in table.items():
#             for l, p in v:
#                 if len(char) == l and re.compile(p).match(char):
#                     return (k, p)
#         return (None, None)
#
#     def convertToStack(self):
#         self.reader.skipBlank()
#         while not self.reader.isEnd():
#             if self.reader.peekNext() == ' ':
#                 self.reader.skipBlank()
#             else:
#                 char2 = self.reader.peek(2)
#                 (syntaxDef, pattern) = self.checkDefinition(self.syntax_definition, char2)
#                 if syntaxDef:
#                     self.reader.read(2)
#                     self.textStack.insert(0, (syntaxDef, char2))
#                     continue
#                 char = self.reader.peekNext()
#                 (syntaxDef, pattern) = self.checkDefinition(self.syntax_definition, char)
#                 if syntaxDef:
#                     self.reader.readNext()
#                     self.textStack.insert(0, (syntaxDef, char))
#                     continue
#                 (stringDef, pattern) = self.checkDefinition(self.string_definition, char)
#                 if stringDef:
#                     word = self.reader.readStringVariable()
#                     self.textStack.insert(0, (stringDef, word))
#                     continue
#                 (varDef, pattern) = self.checkDefinition(self.variable_definiation, char)
#                 if varDef:
#                     word = self.reader.readStringPatternWord(pattern)
#                     self.textStack.insert(0, (varDef, word))
#                     continue
#                 self.raiseError('Scan error, char not allow', (None, self.reader.currentPosition))
#
#     def convertToStackbak(self):
#         self.reader.skipBlank()
#         while not self.reader.isEnd():
#             if self.reader.peekNext() == ' ':
#                 self.reader.skipBlank()
#             elif self.reader.peekNext() == '"' or self.reader.peekNext() == '"':
#                 word = self.reader.readStringVariable()
#                 if word:
#                     self.textStack.insert(0, ('value', word))
#                 else:
#                     word = self.reader.readStringPatternWord("""[\w"']""")
#                     self.textStack.insert(0, ('name', word))
#             elif self.reader.peek(2) == '!=' or self.reader.peek(2) == '>=' or self.reader.peek(
#                     2) == '<=' or self.reader.peek(2) == '!#':
#                 word = self.reader.read(2)
#                 self.textStack.insert(0, ('operator', word))
#             elif self.reader.peekNext() == '(' or self.reader.peekNext() == ')' or self.reader.peekNext() == ',' or self.reader.peekNext() == '|':
#                 word = self.reader.readNext()
#                 self.textStack.insert(0, ('condition', word))
#             elif self.reader.peekNext() == '@' or self.reader.peekNext() == '!' or self.reader.peekNext() == '@' or self.reader.peekNext() == '=':
#                 word = self.reader.readNext()
#                 self.textStack.insert(0, ('operator', word))
#             else:
#                 word = self.reader.readStringPatternWord('\w')
#                 if word:
#                     self.textStack.insert(0, ('name', word))
#                 else:
#                     self.raiseError('Scan error', (None, self.reader.currentPosition))
#
#     def raiseError(self, desc, node):
#         raise Exception('%s at %s' % (desc, node[1]))
#
#     def parsePush(self, node, status, parseFunc, parseEndStatus):
#         self.textStack.pop()
#         status.append(node[1])
#         result = parseFunc(status)
#         status[-1] = parseEndStatus
#         return result
#
#     def parsePop(self, node, status, parseEndStatus):
#         previousChar = self.pair.get(node[1], None)
#         if not previousChar:
#             return
#         if len(status) > 2 and status[-2] == previousChar:
#             self.textStack.pop()
#             status.pop()
#             status[-1] = parseEndStatus
#         else:
#             self.raiseError('Parse error, mismatch %s' % node[1], node)
#
#     def parseSingleCondition(self, status):
#         operator = None
#         fieldName = None
#         value = None
#         status.append('S')
#         finished = False
#         while len(self.textStack) > 0 and status[-1] != 'E':
#             node = self.textStack[-1]
#             if status[-1] == 'S':
#                 if node[0] == 'variable':
#                     status[-1] = 'S1'
#                     fieldName = node[1]
#                     self.textStack.pop()
#                 else:
#                     self.raiseError('Parse error, should be name', node)
#             elif status[-1] == 'S1':
#                 if node[0] == 'operator':
#                     status[-1] = 'S2'
#                     operator = node[1]
#                     self.textStack.pop()
#                 else:
#                     self.raiseError('Parse error, should be operator', node)
#             elif status[-1] == 'S2':
#                 if node[0] == 'string':
#                     value = node[1]
#                     status[-1] = 'E'
#                     self.textStack.pop()
#                 else:
#                     self.raiseError('Parse error, should be value', node)
#         status.pop()
#         print 'Parse router: ', status
#         return ('condition', (operator, fieldName, value))
#
#     def parseCondition(self, status):
#         status.append('S')
#         finished = False
#         left_result = None
#         right_result = None
#         operator = None
#         while len(self.textStack) > 0 and status[-1] != 'E':
#             node = self.textStack[-1]
#             if status[-1] == 'S':
#                 if node[0] == 'condition' and node[1] == '(':
#                     left_result = self.parsePush(node, status, self.parseCondition, 'S1')
#                 elif node[0] == 'variable':
#                     left_result = self.parseSingleCondition(status)
#                     status[-1] = 'S1'
#                 else:
#                     self.raiseError('Parse error, should be nest condition or condition', node)
#             elif status[-1] == 'S1':
#                 right_result = None
#                 if node[0] == 'condition' and node[1] == '|':
#                     # status[-1] = 'S2'
#                     status[-1] = 'S'
#                     print 'find or'
#                     operator = 'or'
#                     self.textStack.pop()
#                     self.priorityStack.append(('or', left_result))
#                 elif node[0] == 'condition' and node[1] == ',':
#                     status[-1] = 'S2'
#                     print 'find and'
#                     operator = 'and'
#                     self.textStack.pop()
#                 elif node[0] == 'condition' and node[1] == ')':
#                     self.parsePop(node, status, 'E')
#                 else:
#                     self.raiseError('Parse error, should be and or bracket', node)
#             elif status[-1] == 'S2':
#                 if node[0] == 'condition' and node[1] == '(':
#                     right_result = self.parsePush(node, status, self.parseCondition, 'S3')
#                 elif node[0] == 'variable':
#                     right_result = self.parseSingleCondition(status)
#                     status[-1] = 'S3'
#                 else:
#                     self.raiseError('Parse error, should be nest condition or condition', node)
#             elif status[-1] == 'S3':
#                 if node[0] == 'condition' and node[1] == ')':
#                     self.parsePop(node, status, 'E')
#                 elif node[0] == 'condition':
#                     if len(status) > 0:
#                         status[-1] = 'S1'
#                         left_result = (operator, left_result, right_result)
#
#                 else:
#                     self.raiseError('Parse error, not be any text here', node)
#         status.pop()
#         print 'Parse router: ', status
#         if operator and right_result:
#             finalResult = ('andor', (operator, left_result, right_result))
#             # finalResult = (operator, left_result, right_result)
#         else:
#             finalResult = left_result
#         while len(self.priorityStack) > 0:
#             (left_operator, left_result_in_stack) = self.priorityStack.pop()
#             finalResult = (left_operator, left_result_in_stack, finalResult)
#         return finalResult
#
#     def parse(self):
#         status = []
#         return self.parseCondition(status)
#
#     def loop(self, result):
#         (type, node) = result[0], result[1]
#         if type == 'andor':
#             return self.loop(node)
#         elif type == 'condition':
#             return self.loop(node)
#         n, l, r = result[0], result[1], result[2]
#         if n == 'and' or n == 'or':
#             left = self.loop(l)
#             right = self.loop(r)
#             if n == 'and':
#                 return '(%s %s %s)' % (left, ' && ', right)
#             else:
#                 return '(%s %s %s)' % (left, ' || ', right)
#         else:
#             return '%s %s %s' % (l, n, r)
#
#     def toDictback(self, result, dict):
#         (type, node) = result[0], result[1]
#         n, l, r = node[0], node[1], node[2]
#         if n == 'and' or n == 'or':
#             self.toDict(l, dict)
#             self.toDict(r, dict)
#         else:
#             opt = {'opt': n, 'low': r}
#             f = dict.get(l, None)
#             if not f:
#                 dict[l] = [opt]
#             else:
#                 dict[l].append(opt)
#             return
#
#     def toDict(self, result):
#         (type, node) = result[0], result[1]
#         if type == 'andor':
#             dict = self.toDict(node)
#             return dict
#         elif type == 'condition':
#             dict = self.toDict(node)
#             return dict
#         n, l, r = result[0], result[1], result[2]
#         if n == 'and' or n == 'or':
#             left = self.toDict(l)
#             right = self.toDict(r)
#             return {'opt': n, 'left': left, 'right': right}
#         else:
#             return {'opt': n, 'field': l, 'value': r}
#
#
# # s = 'name#"a"'
# # # s = 'c="c"'
# # p = Parser(s)
# # print p.textStack
# # result = p.parse()
# # print result
# # print p.loop(result)
# # # option = {}
# # print p.toDict(result)
# # # print option
#
#
# # import sys
# # sys.path.insert(0, '/home/wahaha/coding/python')
#
# import yaml
#
# f = open('./test.yaml')
# x = yaml.load(f)
#
# print type(x)
# print x
#
#
# class User(object):
#     __djangoModel = None
#     firstName = None
#     lastName = None
#     loginName = None
#     email = None
#     phone = None
#     address = None
#     roles = None
#     orgs = None
#     memo = None
#
#     def __init__(self, djangoModel):
#         self.__djangoModel = djangoModel
#
#     # simple save in BP
#     # firstName
#     # lastName
#     # email
#     # phone
#     def set_loginName(self, value):
#         print('set_loginName called')
#
#     def get_loginName(self):
#         return ('', '')
#
#     def set_phone(self):
#         pass
#
#     def get_phone(self):
#         return ('', '')
#
#     def set_address(self):
#         pass
#
#     def get_address(self):
#         return ('', '')
#
#     def set_roles(self):
#         pass
#
#     def get_roles(self):
#         return ('', '')
#
#     def set_orgs(self):
#         pass
#
#     def get_orgs(self):
#         return ('', '')
#
#     def set_memo(self):
#         pass
#
#     def get_memo(self):
#         return ('', '')
#
#
# def SetFieldValue(businessEntity, fieldValue, **configuredData):
#     """
#     This method set value to a field, it will try set_xxx on Business Entity or call SetOrderValue method
#     :param businessEntity: Business Entity object
#     :param fieldValue: value to set
#     :param configuredData: field configurations
#     :return: None
#     """
#     # If required, check whether field value is blank
#     # required = configuredData.get('required', False)
#     # if required and (fieldValue is None or fieldValue.strip() == ''):
#     #     raise Exception(u"不可为空")
#     # # Call set method
#     callName = 'set_%s' % configuredData['fieldKey']
#     if hasattr(businessEntity, callName):
#         # print "call be.%s(fieldValue)" % callName
#         exec ("businessEntity.%s(fieldValue)" % callName)
#     else:
#         # No set method provided
#         # Save by framework according to the configuration
#         SetEntityValue(businessEntity, fieldValue, **configuredData)
#
#
# # Set the entity value based on configuration data
# def SetEntityValue(entity, value, **confData):
#     print('set entity value')
#     return
#     """
#     This method set field value into Django Order model based on field configuration
#     :param orderModel: Order model object
#     :param confField: StdViewLayoutConf object
#     :param value: value that need to be saved
#     :return: won't return any value
#     """
#     storeColumn = confData.get('storeColumn', None)
#     fieldKey = confData.get('fieldKey', None)
#     storeType = confData.get('storeType', None)
#     storeKey = confData.get('storeKey', None)
#     required = confData.get('required', False)
#     fieldColumn = bool(storeColumn) and storeColumn or fieldKey
#     # Check value type
#     if confData['valueType'] == 'Number':
#         try:
#             int(value)
#             float(value)
#         except Exception, e:
#             raise Exception(u"非数字类型")
#     elif confData['valueType'] == 'Boolean':
#         try:
#             bool(value)
#         except Exception, e:
#             raise Exception(u"非布尔类型")
#     else:
#         pass
#     if hasattr(entity, 'orderModel'):
#         orderModel = entity.orderModel
#         if storeType == 'PF' and storeKey:
#             if value:
#                 OrderPFNew_or_update(orderModel, storeKey, BP.objects.get(id=value))
#             else:
#                 OrderPFDelete(orderModel, storeKey, None)
#         elif storeType == 'Customized':
#             if not hasattr(orderModel, 'ordercustomized'):
#                 # If no OrderCustomized record, create one
#                 orderModel.ordercustomized = OrderCustomized()
#                 orderModel.ordercustomized.save()
#                 orderModel.save()
#             if hasattr(orderModel.ordercustomized, fieldColumn):
#                 if confData['fieldType'] == 'IF':
#                     if value:
#                         if int(value) > 0:
#                             uploadFilesTemp = UploadFilesTemp.objects.get(id=value)
#                             exec (
#                                 "orderModel.ordercustomized.%s.save(uploadFilesTemp.imageFile._get_path().split('/')[-1],uploadFilesTemp.imageFile)" % (
#                                     fieldColumn,))
#                             filepath = uploadFilesTemp.imageFile.path
#                             uploadFilesTemp.delete();
#                             os.remove(filepath)
#                         else:
#                             exec ("orderModel.ordercustomized.%s=None" % (fieldColumn,))
#                 elif confData['fieldType'] == 'FI':
#                     if value:
#                         if int(value) > 0:
#                             uploadFilesTemp = UploadFilesTemp.objects.get(id=value)
#                             exec (
#                                 "orderModel.ordercustomized.%s.save(uploadFilesTemp.normalFile._get_path().split('/')[-1],uploadFilesTemp.normalFile)" % (
#                                     fieldColumn,))
#                             filepath = uploadFilesTemp.normalFile.path
#                             uploadFilesTemp.delete();
#                             os.remove(filepath)
#                         else:
#                             exec ("orderModel.ordercustomized.%s=None" % (fieldColumn,))
#                 else:
#                     if value is None:
#                         exec ("orderModel.ordercustomized.%s=None" % fieldColumn)
#                     else:
#                         if confData['valueType'] in ['Number', 'Boolean']:
#                             # Number type
#                             exec ("orderModel.ordercustomized.%s=%s" % (fieldColumn, value))
#                         else:
#                             # String type
#                             exec ("orderModel.ordercustomized.%s='%s'" % (fieldColumn, value))
#                 orderModel.ordercustomized.save()
#             else:
#                 raise Exception(u"%s not found on ordercustomized" % fieldColumn)
#         elif storeType == 'MultipleValue':
#             # Value is a json object
#             jsonValue = json.loads(value)
#             # Remove records whose id not in current jsonValue
#             ids = []
#             newToCreate = []
#             for value in jsonValue:
#                 if str(value['id']).startswith('new'):
#                     newToCreate.append(value)
#                 else:
#                     ids.append(value['id'])
#             if ids:
#                 for order in orderModel.ordermultiplevaluefield_set.filter(~Q(id__in=ids),
#                                                                            Q(field__fieldKey=confData['fieldKey'])):
#                     order.delete()
#             if not jsonValue:
#                 for order in orderModel.ordermultiplevaluefield_set.filter(Q(field__fieldKey=confData['fieldKey'])):
#                     order.delete()
#             # Add new record if any
#             for value in newToCreate:
#                 omvf = OrderMultipleValueField()
#                 omvf.order = orderModel
#                 omvf.field = orderModel.type.orderfielddef_set.filter(fieldKey=confData['fieldKey'])[0]
#                 omvf.charValue1 = value.get('charValue1', None)
#                 omvf.charValue2 = value.get('charValue2', None)
#                 orderModel.ordermultiplevaluefield_set.add(omvf)
#                 orderModel.save()
#         elif storeType == 'Activity':
#             if not hasattr(orderModel, 'activity'):
#                 # If no OrderCustomized record, create one
#                 # orderModel.activity = Activity()
#                 activity = Activity()
#                 activity.order = orderModel
#                 activity.save()
#                 orderModel.activity = activity
#                 orderModel.save()
#             orderModel.activity.order = orderModel
#             orderModel.activity.save()
#             if hasattr(orderModel.activity, fieldColumn):
#                 if value is None:
#                     exec ("orderModel.activity.%s=None" % fieldColumn)
#                 else:
#                     if confData['valueType'] in ['Number', 'Boolean']:
#                         # Number type
#                         exec ("orderModel.activity.%s=%s" % (fieldColumn, value))
#                     else:
#                         # String type
#                         exec ("orderModel.activity.%s='%s'" % (fieldColumn, value))
#                 orderModel.activity.save()
#             else:
#                 raise Exception(u"%s not found on ordercustomized" % fieldColumn)
#         elif storeType == 'Text' and storeKey:
#             if value:
#                 newText = OrderText()
#                 newText.order = orderModel
#                 newText.type = TextType.objects.get(pk=storeKey)
#                 newText.content = value
#                 newText.createdBy = orderModel.updatedBy
#                 newText.save()
#         else:
#             # Check field on Order model
#             if hasattr(orderModel, fieldColumn):
#                 if value is None:
#                     exec ("orderModel.%s=None" % fieldColumn)
#                 else:
#                     if confData['valueType'] in ['Number', 'Boolean']:
#                         exec ("orderModel.%s=%s" % (fieldColumn, value))
#                     else:
#                         exec ("orderModel.%s='%s'" % (fieldColumn, value))
#                 orderModel.save()
#             else:
#                 raise Exception(u'order上未找到字段%s' % fieldColumn)
#     elif hasattr(entity, 'bpModel'):
#         bpModel = entity.bpModel
#         if storeType == 'Customized':
#             if not hasattr(bpModel, 'bpcustomized'):
#                 # If no BPCustomized record, create one
#                 bpModel.bpcustomized = BPCustomized()
#                 bpModel.bpcustomized.save()
#                 bpModel.save()
#             else:
#                 if bpModel.bpcustomized.id is None:
#                     bpModel.bpcustomized.bp = bpModel
#                     bpModel.bpcustomized.save()
#                     bpModel.save()
#             if hasattr(bpModel.bpcustomized, fieldColumn):
#                 if confData['fieldType'] == 'IF':
#                     if value:
#                         if int(value) > 0:
#                             uploadFilesTemp = UploadFilesTemp.objects.get(id=value)
#                             exec (
#                                 "bpModel.bpcustomized.%s.save(uploadFilesTemp.imageFile._get_path().split('/')[-1],uploadFilesTemp.imageFile)" % (
#                                     fieldColumn,))
#                             filepath = uploadFilesTemp.imageFile.path
#                             uploadFilesTemp.delete();
#                             os.remove(filepath)
#                         else:
#                             exec ("bpModel.bpcustomized.%s=None" % (fieldColumn,))
#                 elif confData['fieldType'] == 'FI':
#                     if value:
#                         if int(value) > 0:
#                             uploadFilesTemp = UploadFilesTemp.objects.get(id=value)
#                             exec (
#                                 "bpModel.bpcustomized.%s.save(uploadFilesTemp.normalFile._get_path().split('/')[-1],uploadFilesTemp.normalFile)" % (
#                                     fieldColumn,))
#                             filepath = uploadFilesTemp.normalFile.path
#                             uploadFilesTemp.delete();
#                             os.remove(filepath)
#                         else:
#                             exec ("bpModel.bpcustomized.%s=None" % (fieldColumn,))
#                 else:
#                     if value is None:
#                         exec ("bpModel.bpcustomized.%s=None" % fieldColumn)
#                     else:
#                         if confData['valueType'] in ['Number', 'Boolean']:
#                             # Number type
#                             exec ("bpModel.ordercustomized.%s=%s" % (fieldColumn, value))
#                         else:
#                             # String type
#                             exec ("bpModel.ordercustomized.%s='%s'" % (fieldColumn, value))
#                 bpModel.bpcustomized.save()
#             else:
#                 raise Exception(u"%s not found on bpcustomized" % fieldColumn)
#         elif storeType == 'Text' and storeKey:
#             newText = BPText()
#             newText.bp = bpModel
#             newText.type = BPTextType.objects.get(pk=storeKey)
#             newText.content = value
#             newText.createdBy = bpModel.updatedBy
#             newText.save()
#         else:
#             # Check field on BP model
#             if hasattr(bpModel, fieldColumn):
#                 if value is None:
#                     exec ("bpModel.%s=None" % fieldColumn)
#                 else:
#                     if confData['valueType'] in ['Number', 'Boolean']:
#                         exec ("bpModel.%s=%s" % (fieldColumn, value))
#                     else:
#                         exec ("bpModel.%s='%s'" % (fieldColumn, value))
#                 bpModel.save()
#             else:
#                 raise Exception(u'bp上未找到字段%s' % fieldColumn)
#
#
# user = User(object)
# SetFieldValue(user, 'fn', **{'fieldKey':'loginName'})