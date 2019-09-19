import pytest

from interpreter.commands import Command

from interpreter.stacks import Stack, Item

class TestStacks:
    def test_init(self):
        stack = Stack()
        assert stack.items == []
        assert stack.local_var == {}
        assert stack.local_func == {}

    def test_push(self):
        stack = Stack()
        item = Item('a',1)
        stack.push(item)
        stack.push(1)
        assert len(stack.items) == 2
        assert len(stack.local_var) == 1
        assert len(stack.local_func) == 0

    def test_multi_push(self):
        stack = Stack()
        for i in range(1,11,1):
            stack.push(Item('a',1))
        assert len(stack) == 10
        assert len(stack.local_var) == 1

    def test_pop_error(self):
        stack = Stack()
        stack.pop()
        assert len(stack.items) == 1
        assert stack.items.pop() == ':error:'

    def test_pop(self):
        stack = Stack()
        stack.items.append(1)
        assert len(stack.items) == 1
        assert stack.pop() == 1
        assert len(stack.items) == 0

    def test_same_type(self):
        stack = Stack()
        a = Item('a',1)
        b = Item('b',2)
        c = Item('c','3')
        d = Item('d','4')
        assert stack.same_type(1,1) == True
        assert stack.same_type(a,1) == True
        assert stack.same_type(1,a) == True
        assert stack.same_type(a,b) == True
        assert stack.same_type(1,c) == False
        assert stack.same_type(c,1) == False
        assert stack.same_type(c,d) == True
        assert stack.same_type('','') == True

    def test_match_type(self):
        stack = Stack()
        a = Item('a',1)
        b = Item('b',2)
        c = Item('c','3')
        d = Item('d','4')
        assert stack.match_type(int,1,1) == True
        assert stack.match_type(int,a,1) == True
        assert stack.match_type(int,1,a) == True
        assert stack.match_type(int,a,b) == True
        assert stack.match_type(int,1,c) == False
        assert stack.match_type(int,c,1) == False
        assert stack.match_type(int,c,d) == False
        assert stack.match_type(int,'','') == False
        assert stack.match_type(int,True,True) == True  # language design...
        assert stack.match_type(bool,1,1) == False  # language design...


    def test_arithmetic_add(self):
        stack = Stack()
        cmd = Command.ADD
        a = 1
        b = 2
        x = Item('x', 3)
        y = Item('y', 4)
        err = ':error:'
        assert stack.arithmetic(cmd,a,b) == 3
        assert stack.arithmetic(cmd,a,x) == 4
        assert stack.arithmetic(cmd,x,b) == 5
        assert stack.arithmetic(cmd,x,y) == 7
        assert stack.arithmetic(cmd,x,'b') == err
        assert stack.arithmetic(cmd,'a',y) == err
        assert stack.arithmetic(cmd,'a','b') == err

    def test_arithmetic_sub(self):
        stack = Stack()
        cmd = Command.SUB
        a = 4
        b = 3
        x = Item('x', 2)
        y = Item('y', 1)
        err = ':error:'
        assert stack.arithmetic(cmd,b,a) == 1
        assert stack.arithmetic(cmd,x,a) == 2
        assert stack.arithmetic(cmd,x,b) == 1
        assert stack.arithmetic(cmd,x,y) == -1
        assert stack.arithmetic(cmd,x,'b') == err
        assert stack.arithmetic(cmd,'a',y) == err
        assert stack.arithmetic(cmd,'a','b') == err

    def test_arithmetic_mul(self):
        stack = Stack()
        cmd = Command.MUL
        a = 4
        b = 3
        x = Item('x', 2)
        y = Item('y', 1)
        err = ':error:'
        assert stack.arithmetic(cmd,a,b) == 12
        assert stack.arithmetic(cmd,a,x) == 8
        assert stack.arithmetic(cmd,x,b) == 6
        assert stack.arithmetic(cmd,x,y) == 2
        assert stack.arithmetic(cmd,x,'b') == err
        assert stack.arithmetic(cmd,'a',y) == err
        assert stack.arithmetic(cmd,'a','b') == err

    def test_arithmetic_div(self):
        stack = Stack()
        cmd = Command.DIV
        a = 100
        b = 200
        y = Item('y', 50)
        x = Item('x', 300)
        z = Item('z', 0)
        err = ':error:'
        assert stack.arithmetic(cmd,a,b) == 2
        assert stack.arithmetic(cmd,a,x) == 3
        assert stack.arithmetic(cmd,y,b) == 4
        assert stack.arithmetic(cmd,y,x) == 6
        assert stack.arithmetic(cmd,a,0) == 0
        assert stack.arithmetic(cmd,0,y) == err
        assert stack.arithmetic(cmd,z,a) == err
        assert stack.arithmetic(cmd,x,'b') == err
        assert stack.arithmetic(cmd,'a',y) == err
        assert stack.arithmetic(cmd,'a','b') == err


    def test_arithmetic_rem(self):
        stack = Stack()
        cmd = Command.REM
        b = 100
        a = 2
        x = Item('x', 50)
        y = Item('y', 25)
        z = Item('z', 0)
        err = ':error:'
        assert stack.arithmetic(cmd,a,b) == 0
        assert stack.arithmetic(cmd,a,x) == 0
        assert stack.arithmetic(cmd,x,b) == 0
        assert stack.arithmetic(cmd,y,x) == 0
        assert stack.arithmetic(cmd,a,0) == 0
        assert stack.arithmetic(cmd,0,y) == err
        assert stack.arithmetic(cmd,z,a) == err
        assert stack.arithmetic(cmd,x,'b') == err
        assert stack.arithmetic(cmd,'a',y) == err
        assert stack.arithmetic(cmd,'a','b') == err

    def test_arithmetic_neg(self):
        stack = Stack()
        cmd = Command.NEG
        a = 1
        b = Item('b', 2)
        err = ':error:'
        assert stack.arithmetic(cmd,a,0) == -1  # ignores third arg
        assert stack.arithmetic(cmd,b,0) == -2
        assert stack.arithmetic(cmd,a,'b') == err
        assert stack.arithmetic(cmd,'a',b) == err
        assert stack.arithmetic(cmd,'a','b') == err

    def test_math_empty_neg(self):
        stack = Stack()
        stack.math(Command.NEG)
        err = ':error:'
        assert stack.items.pop() == err

    def test_math_neg(self):
        stack = Stack()
        stack.push(10)
        stack.math(Command.NEG)
        assert len(stack) == 1
        assert stack.pop() == -10

    def test_math_add(self):
        stack = Stack()
        for x,y in zip(range(10,21,1),range(10,-11,-1)):
            stack.push(x)
            stack.push(y)
            stack.math(Command.ADD)
            assert len(stack) == 1
            assert stack.pop() == x+y
        assert len(stack) == 0

    def test_math_sub(self):
        stack = Stack()
        for x,y in zip(range(10,21,1),range(10,-11,-1)):
            stack.push(x)
            stack.push(y)
            stack.math(Command.SUB)
            assert len(stack) == 1
            assert stack.pop() == x-y
        assert len(stack) == 0

    def test_math_mul(self):
        stack = Stack()
        for x,y in zip(range(10,21,1),range(10,-11,-1)):
            stack.push(x)
            stack.push(y)
            stack.math(Command.MUL)
            assert len(stack) == 1
            assert stack.pop() == x*y
        assert len(stack) == 0

    def test_math_div(self):
        stack = Stack()
        for x,y in zip(range(0,11,1),range(-10,0,-1)):
            stack.push(x)
            stack.push(y)
            stack.math(Command.DIV)
            assert len(stack) == 1
            assert stack.pop() == x // y
        assert len(stack) == 0
        stack.push(1)
        stack.push(0)
        stack.math(Command.DIV)
        assert stack.pop() == ':error:'
        assert stack.pop() == 0
        assert stack.pop() == 1
        n = Item('n',1)
        z = Item('z',0)
        stack.push(n)
        stack.push(z)
        stack.math(Command.DIV)
        assert stack.pop() == ':error:'
        z2 = stack.pop()
        n1 = stack.pop()
        assert isinstance(n1, Item)
        assert isinstance(z2, Item)
        assert n1.value == n.value
        assert z2.value == z.value

    def test_math_rem(self):
        stack = Stack()
        for x,y in zip(range(0,11,1),range(-10,0,-1)):
            stack.push(x)
            stack.push(y)
            stack.math(Command.REM)
            assert len(stack) == 1
            assert stack.pop() == x % y
        assert len(stack) == 0
        stack.push(1)
        stack.push(0)
        stack.math(Command.REM)
        assert stack.pop() == ':error:'
        assert stack.pop() == 0
        assert stack.pop() == 1
        n = Item('n',1)
        z = Item('z',0)
        stack.push(n)
        stack.push(z)
        stack.math(Command.REM)
        assert stack.pop() == ':error:'
        z2 = stack.pop()
        n1 = stack.pop()
        assert isinstance(n1, Item)
        assert isinstance(z2, Item)
        assert n1.value == n.value
        assert z2.value == z.value

    def test_logic_not(self):
        stack = Stack()
        cmd = Command.NOT
        t = True
        f = Item('f', False)
        assert stack.logic(cmd,None,t,None) == False
        assert stack.logic(cmd,None,f,None) == True
        assert stack.logic(cmd,None,'some',None) == ':error:'
        assert stack.logic(cmd,None,1,None) == ':error:'

    def test_logic_if(self):
        stack = Stack()
        cmd = Command.IF
        t = Item('t', True)
        f = Item('f', False)
        assert stack.logic(cmd,True,2,1) == 1
        assert stack.logic(cmd,False,2,1) == 2
        assert stack.logic(cmd,t,2,1) == 1
        assert stack.logic(cmd,f,2,1) == 2
        assert stack.logic(cmd,1,2,1) == ':error:'
        assert stack.logic(cmd,0,2,1) == ':error:'
        assert stack.logic(cmd,None,None,None) == ':error:'

    def test_logic_and(self):
        stack = Stack()
        cmd = Command.AND
        t = Item('t', True)
        f = Item('f', False)
        assert stack.logic(cmd,None,True,True) == True
        assert stack.logic(cmd,None,True,False) == False
        assert stack.logic(cmd,None,False,True) == False
        assert stack.logic(cmd,None,False,False) == False
        assert stack.logic(cmd,None,t,t) == True
        assert stack.logic(cmd,None,t,f) == False
        assert stack.logic(cmd,None,f,t) == False
        assert stack.logic(cmd,None,f,f) == False
        assert stack.logic(cmd,None,1,1) == ':error:'
        assert stack.logic(cmd,None,0,1) == ':error:'
        assert stack.logic(cmd,None,None,None) == ':error:'

    def test_logic_or(self):
        stack = Stack()
        cmd = Command.OR
        t = Item('t', True)
        f = Item('f', False)
        assert stack.logic(cmd,None,True,True) == True
        assert stack.logic(cmd,None,True,False) == True
        assert stack.logic(cmd,None,False,True) == True
        assert stack.logic(cmd,None,False,False) == False
        assert stack.logic(cmd,None,t,t) == True
        assert stack.logic(cmd,None,t,f) == True
        assert stack.logic(cmd,None,f,t) == True
        assert stack.logic(cmd,None,f,f) == False
        assert stack.logic(cmd,None,1,1) == ':error:'
        assert stack.logic(cmd,None,0,1) == ':error:'
        assert stack.logic(cmd,None,None,None) == ':error:'

    def test_logic_eq(self):
        stack = Stack()
        cmd = Command.EQUAL
        a = Item('a', 1)
        b = Item('b', 1)
        c = Item('a', 2)
        assert stack.logic(cmd,None,b,a) == True
        assert stack.logic(cmd,None,a,b) == True
        assert stack.logic(cmd,None,b,c) == False
        assert stack.logic(cmd,None,1,1) == True
        assert stack.logic(cmd,None,1,0) == False
        assert stack.logic(cmd,None,True,True) == ':error:'
        assert stack.logic(cmd,None,False,False) == ':error:'
        assert stack.logic(cmd,None,None,None) == ':error:'

    def test_logic_lt(self):
        stack = Stack()
        cmd = Command.LESS
        a = Item('a', 1)
        b = Item('b', 2)
        assert stack.logic(cmd,None,b,a) == True
        assert stack.logic(cmd,None,a,b) == False
        assert stack.logic(cmd,None,1,2) == False
        assert stack.logic(cmd,None,2,1) == True
        assert stack.logic(cmd,None,0,0) == False
        assert stack.logic(cmd,None,True,True) == ':error:'
        assert stack.logic(cmd,None,False,True) == ':error:'
        assert stack.logic(cmd,None,True,False) == ':error:'
        assert stack.logic(cmd,None,False,False) == ':error:'
        assert stack.logic(cmd,None,None,None) == ':error:'

    def test_logical_not(self):
        stack = Stack()
        cmd = Command.NOT
        # expected
        stack.push(True)  # bottom of stack
        stack.push(False)  # top of stack
        assert len(stack) == 2
        stack.logical(cmd)  # call
        assert stack.pop() == True  # changed item
        assert stack.pop() == True  # unchanged item
        assert len(stack) == 0
        # empty stack call
        stack.logical(cmd)
        assert stack.pop() == ':error:'
        # expected
        stack.push(True)  # bottom of stack
        stack.push(False)  # top of stack
        assert len(stack) == 2
        stack.logical(cmd)  # call
        stack.logical(cmd)  # call
        assert stack.pop() == False  # changed item
        assert stack.pop() == True  # unchanged item
        # Item
        stack.push(Item('t', True))  # top of stack
        stack.logical(cmd)  # call
        assert stack.pop() == False  # changed item
        # error
        stack.push(1)  # unsupported
        stack.logical(cmd)  # call
        assert len(stack) == 2
        assert stack.pop() == ':error:'
        assert stack.pop() == 1

    def test_logical_if(self):
        stack = Stack()
        cmd = Command.IF
        # expected
        stack.push(True)  # z, bottom of stack
        stack.push(2)  # y
        stack.push(1)  # x, top of stack
        stack.logical(cmd)  # call
        assert len(stack) == 1
        assert stack.pop() == 1
        # error
        stack.push(1)  # z, unsupported, bottom of stack
        stack.push(2)  # y
        stack.push(True)  # x, top of stack
        stack.logical(cmd)  # call
        assert len(stack) == 4
        assert stack.pop() == ':error:'

    def test_logical_and(self):
        stack = Stack()
        cmd = Command.AND
        # expected
        stack.push(True)  # x, bottom of stack
        stack.push(True)  # y, top of stack
        stack.logical(cmd)  # call
        assert stack.pop() == True  # result
        stack.push(True)  # x, bottom of stack
        stack.push(False)  # y, top of stack
        stack.logical(cmd)  # call
        assert stack.pop() == False  # result
        stack.push(False)  # x, bottom of stack
        stack.push(True)  # y, top of stack
        stack.logical(cmd)  # call
        assert stack.pop() == False  # result
        stack.push(False)  # x, bottom of stack
        stack.push(False)  # y, top of stack
        stack.logical(cmd)  # call
        assert stack.pop() == False  # result
        # Item
        t = Item('t', True)
        f = Item('f', False)
        stack.push(t)  # x, bottom of stack
        stack.push(t)  # y, top of stack
        stack.logical(cmd)  # call
        assert stack.pop() == True  # result
        stack.push(t)  # x, bottom of stack
        stack.push(f)  # y, top of stack
        stack.logical(cmd)  # call
        assert stack.pop() == False  # result
        stack.push(f)  # x, bottom of stack
        stack.push(t)  # y, top of stack
        stack.logical(cmd)  # call
        assert stack.pop() == False  # result
        stack.push(f)  # x, bottom of stack
        stack.push(f)  # y, top of stack
        stack.logical(cmd)  # call
        assert stack.pop() == False  # result
        # error
        stack.push(2)  # x, unsupported, bottom of stack
        stack.push(1)  # y, unsupported, top of stack
        stack.logical(cmd)  # call
        assert stack.pop() == ':error:'  # result
        assert stack.pop() == 1  # result
        assert stack.pop() == 2  # result

    def test_logical_and(self):
        stack = Stack()
        cmd = Command.OR
        # expected
        stack.push(True)  # x, bottom of stack
        stack.push(True)  # y, top of stack
        stack.logical(cmd)  # call
        assert stack.pop() == True  # result
        stack.push(True)  # x, bottom of stack
        stack.push(False)  # y, top of stack
        stack.logical(cmd)  # call
        assert stack.pop() == True  # result
        stack.push(False)  # x, bottom of stack
        stack.push(True)  # y, top of stack
        stack.logical(cmd)  # call
        assert stack.pop() == True  # result
        stack.push(False)  # x, bottom of stack
        stack.push(False)  # y, top of stack
        stack.logical(cmd)  # call
        assert stack.pop() == False  # result
        # Items
        t = Item('t', True)
        f = Item('f', False)
        stack.push(t)  # x, bottom of stack
        stack.push(t)  # y, top of stack
        stack.logical(cmd)  # call
        assert stack.pop() == True  # result
        stack.push(t)  # x, bottom of stack
        stack.push(f)  # y, top of stack
        stack.logical(cmd)  # call
        assert stack.pop() == True  # result
        stack.push(f)  # x, bottom of stack
        stack.push(t)  # y, top of stack
        stack.logical(cmd)  # call
        assert stack.pop() == True  # result
        stack.push(f)  # x, bottom of stack
        stack.push(f)  # y, top of stack
        stack.logical(cmd)  # call
        assert stack.pop() == False  # result
        # error
        stack.push(2)  # x, unsupported, bottom of stack
        stack.push(1)  # y, unsupported, top of stack
        stack.logical(cmd)  # call
        assert stack.pop() == ':error:'  # result
        assert stack.pop() == 1  # result
        assert stack.pop() == 2  # result

    def test_logical_eq(self):
        stack = Stack()
        cmd = Command.EQUAL
        # same values
        stack.push(1)  # x, bottom of stack
        stack.push(1)  # y, top of stack
        stack.logical(cmd)  # call
        assert stack.pop() == True  # result
        # different values
        stack.push(1)  # x, bottom of stack
        stack.push(2)  # y, top of stack
        stack.logical(cmd)  # call
        assert stack.pop() == False  # result
        # Items
        x = Item('x', 1)
        y = Item('y', 1)
        z = Item('z', 2)
        # same item value
        stack.push(x)  # x, bottom of stack
        stack.push(y)  # y, top of stack
        stack.logical(cmd)  # call
        assert stack.pop() == True  # result
        # different item value
        stack.push(z)  # z, bottom of stack
        stack.push(y)  # y, top of stack
        stack.logical(cmd)  # call
        assert stack.pop() == False  # result
        # error
        stack.push(True)  # x, unsupported, bottom of stack
        stack.push(True)  # y, unsupported, top of stack
        stack.logical(cmd)  # call
        assert stack.pop() == ':error:'  # result
        assert stack.pop() == True  # result
        assert stack.pop() == True  # result

    def test_logical_lt(self):
        stack = Stack()
        cmd = Command.LESS
        # expected
        stack.push(1)  # x, bottom of stack
        stack.push(2)  # y, top of stack
        stack.logical(cmd)  # call
        assert stack.pop() == True  # result
        # different values
        stack.push(2)  # x, bottom of stack
        stack.push(1)  # y, top of stack
        stack.logical(cmd)  # call
        assert stack.pop() == False  # result
        # Items
        x = Item('x', 1)
        y = Item('y', 2)
        # same item value
        stack.push(x)  # x, bottom of stack
        stack.push(y)  # y, top of stack
        stack.logical(cmd)  # call
        assert stack.pop() == True  # result
        # different item value
        stack.push(y)  # y, bottom of stack
        stack.push(x)  # x, top of stack
        stack.logical(cmd)  # call
        assert stack.pop() == False  # result
        # error
        stack.push(True)  # x, unsupported, bottom of stack
        stack.push(True)  # y, unsupported, top of stack
        stack.logical(cmd)  # call
        assert stack.pop() == ':error:'  # result
        assert stack.pop() == True  # result
        assert stack.pop() == True  # result

    def test_swap(self):
        stack = Stack()
        stack.push(1)  # x, bottom of stack
        stack.push(2)  # y, top of stack
        stack.swap()  # call
        assert stack.pop() == 1  # result
        assert stack.pop() == 2  # result

    def test_bind(self):
        stack = Stack()
        # expected
        var_name = 'a'
        var = Item(var_name,None)
        stack.push(var)  # bottom of stack
        stack.push(1)  # value to be assigned to var, top of stack
        updated_var = stack.bind()  # call
        assert stack.pop() == ':unit:'  # result
        assert updated_var.value == 1
        assert len(stack) == 0
        assert var_name in stack.local_var
        assert len(stack.local_var) == 1
        # expected
        var1_name = 'b'
        var1 = Item(var1_name,1)
        var2 = Item('c',2)
        stack.push(var1)  # bottom of stack
        stack.push(var2)  # value to be assigned to var1, top of stack
        updated_var1 = stack.bind()
        assert stack.pop() == ':unit:'
        assert updated_var1.value == 2
        assert len(stack) == 0
        assert var_name in stack.local_var
        assert len(stack.local_var) == 3
        # error
        stack.push(Item('e',None))
        stack.push(':error:')  # can't assign variable to an error
        assert stack.bind() == ':error:'  # call and result
        assert len(stack) == 3
        assert stack.pop() == ':error:'  # result
        assert stack.pop() == ':error:'  # previous value
        stack.push(Item('d', None))  # can't assign a variable to an empty variable
        assert stack.bind() == ':error:'  # call and result
        assert len(stack) == 3
        assert stack.pop() == ':error:'  # result
        # unit

    def test_create_func(self):
        pass

    def test_create_io(self):
        pass

    def test_fill_func(self):
        pass
