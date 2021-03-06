import Interpreter
import array
from Exceptions import *

builtIns = {
	'+'  : lambda x: reduce(lambda d,y: d+y, x),
	'-'  : lambda x: reduce(lambda d,y: d-y, x),
	'*'  : lambda x: reduce(lambda d,y: d*y, x),
	'/'  : lambda x: reduce(lambda d,y: d/float(y), x),

	'<'  : lambda x: evalBoolExpr(x, '<'),
	'>'  : lambda x: evalBoolExpr(x, '>'),
	'<=' : lambda x: evalBoolExpr(x, '<='),
	'>=' : lambda x: evalBoolExpr(x, '>='),
	'=' : lambda x: evalEq(x),
	
	'not': lambda x: evalNot(x),
	'and' : lambda x: evalAnd(x),
	'or' : lambda x: evalOr(x),

	'first'    : lambda x: x[0][0],
	'rest'    : lambda x: x[0][1:],
	'substring' : lambda x: x[2][x[0]:x[1]],
	'nth'    : lambda x: x[1][x[0]],
	'length' : lambda x: evalLength(x[0]),

	'list' : lambda x: evalList(x),
	#'vector' : lambda x: evalVector(x),
	'map' : lambda x: evalMap(x),
	'set' : lambda x: evalSet(x),
        'arraymap' : lambda x: evalArrayMap(x),
	
	'println'  : lambda x: evalPrint(x[0]),
	'def'   : lambda x: evalSetq(x),

	'if'	 : lambda x: (x[2], x[1])[x[0] != "nil" and x[0] != "false"]
}

def evalBoolExpr(x, sign):
	for i in range(len(x)-1):
		if not eval(str(x[i]) + " " + str(sign) + " " + str(x[i+1])):
			return "false"
	return "true"

def evalEq(x):
	if len(x) != 2 or x[0]==None or x[1]==None:
		raise FunctionNotFound
	if x[0] == x[1]:
		return "true"
	else:
		return "false"

def evalNot(x):
	if len(x) != 1 or x[0]==None:
		raise FunctionNotFound
	return "true" if x[0] == "false" else "false"

def evalAnd(x):
	for i in range(len(x)):
		if x[i] == "false" or x[i]=="nil":
			return "false"
	return x[len(x)-1]

def evalOr(x):
	for i in range(len(x)):
		if x[i] != "false" and x[i] != "nil":
			return x[i]
	return "false"

def evalLength(x):
	if(type(x) == str):
		return len(x)-2
	else:
		return len(x)

def evalPrint(x):
	print x
	return x

def evalSetq(x):
	if Interpreter.Interpreter.globalMemory.set(x[0], x[1]) == False:
		Interpreter.Interpreter.globalMemory.insert(x[0], x[1])
	return x[1]
	
def evalList(x):
    return list(x)

#def evalVector(x):
#	return list(x)

def evalMap(x):
        retList=list()
        if len(x)!=3:
		raise FunctionNotFound
	if x[0] not in list(builtIns):
                raise FunctionNotFound
        if (not isinstance(x[1],list)) or (not isinstance(x[2],list)):
                raise FunctionNotFound
        if len(x[1])!=len(x[2]):
                raise FunctionNotFound
        for i in range(0, len(x)-1):
                retList.append(builtIns[x[0]]([x[1][i],x[2][i]]))
        return retList

def evalSet(x):
	if len(x)>1:
		raise FunctionNotFound
	retSet=set()
	for elem in x[0]:
		retSet.add(elem)
	return retSet

def evalArrayMap(x):
        if(len(x)%2!=0):
                raise FunctionNotFound
	retDict=dict()
	i=0
	while i < len(x):
		retDict[x[i]]=x[i+1]
		i+=2
	return retDict
