import AST
from Memory import *
from Exceptions import  *
from visit import *
from BuiltInFunctions import builtIns

class Interpreter(object):

    globalMemory = MemoryStack(Memory("global"))
    functionMemory = MemoryStack()
    functions = []

    globalMemory.insert("nil", "nil")
    globalMemory.insert("true", "true")
    globalMemory.insert("false", "false")


    @on('node')
    def visit(self, node):
        pass

    @when(AST.Input)
    def visit(self, node):
        for x in range(len(node.expr_list)):
            res = node.expr_list[x].accept2(self)
            if(type(res) == Exception):
                print res
                return
        print node.expr_list[-1]


    @when(AST.Expression)
    def visit(self, node):
        if(isinstance(node, AST.IdName)):
            print Interpreter.evalNode(self, node.value.name)
        map(lambda x: x.accept2(self), node.args)
        function = None
        try:            
            if(node.function_name == 'def'):
                if len(node.args) != 2:
                    raise FunctionNotFound
                res = builtIns['def']([node.args[0].value.name, Interpreter.evalNode(self, node.args[1])])
            else:
                if(node.function_name not in builtIns):
                    raise FunctionNotFound
                res = builtIns[node.function_name](map(lambda x: Interpreter.evalNode(self, x), node.args))
            node.return_value = res
            return res
            # raise ReturnValueException(node.return_value) #TO TYLKO JESLI BEDZIEMY CHCIELI OBSLUZYC RETURN!
        except (FunctionNotFound, TypeError):
            for func in Interpreter.functions:
                if (func.fun_name == node.function_name):
                    function = func
                    break
            if (function == None):
                return Exception("Wrong arguments")
            Interpreter.functionMemory.push(Memory(node.function_name + "_scope"))
            for i in range(len(function.args_list)):
                value = Interpreter.evalNode(self,node.args[i])
                Interpreter.functionMemory.insert(function.args_list[i].value.name, value)
            retval = None
            # try:
            for i in range(len(function.instr_list)):
                retval = function.instr_list[i].accept2(self)
            # except ReturnValueException as e:
            #     node.return_value = e.value
            #     return e.value
            node.return_value = retval
            Interpreter.functionMemory.pop()
            return retval  

    @when(AST.List)
    def visit(self, node):
        return map(lambda x: x.accept2(self), node.arguments)

    @when(AST.Atom)
    def visit(self, node):
        if(isinstance(node.value, AST.IdName)):
            node.idRetval = Interpreter.evalNode(self, node.value)
            return node.idRetval
        return node.value

    @when(AST.IdName)
    def visit(self, node):
        return Interpreter.evalNode(self, node)
    
    @when(AST.Const)
    def visit(self, node):
        return node.value

    @when(AST.Function)
    def visit(self, node):
        Interpreter.functions.append(node)

    @when(AST.WhileInstr)
    def visit(self, node):
        retval = None
        while (node.condition.accept2(self) == "nil"):
            map(lambda x: x.accept2(self), node.instructions[:-1])
            retval = node.instructions[-1].accept2(self)
        node.return_value = retval
        return retval



    @classmethod
    def current_scope(cls):
        if Interpreter.functionMemory.stack:
            return Interpreter.functionMemory
        else:
            return Interpreter.globalMemory

    @classmethod
    def evalNode(cls, self, node):
        value = None
        if (isinstance(node, AST.Atom) and isinstance(node.value, AST.IdName)):
            value = Interpreter.current_scope().get(node.value.name)
            if value == None:
                value = Interpreter.globalMemory.get(node.value.name)
        elif (isinstance(node, AST.IdName)):
            value = Interpreter.current_scope().get(node.name)
            if value == None:
                value = Interpreter.globalMemory.get(node.name)
        elif isinstance(node, AST.Expression):
            return node.accept2(self)
        elif isinstance(node, AST.List):
            return node.accept2(self)
        elif node:
            value = node.accept2(self)

        return value
