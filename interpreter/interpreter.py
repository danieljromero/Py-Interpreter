"""
A .txt file interpreter written in Python 3.
Copyright (C) 2017  Daniel Romero

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from enum import Enum


class Name:
    def __init__(self, name, value):
        self.name = name
        self.value = value
        self.alias = ""

    def set_alias(self, var_name):
        self.alias = var_name

    def get_name(self):
        return self.name

    def get_val(self):
        return self.value

    def get_alias(self):
        return self.alias


class Command(Enum):
    PUSH = "PUSH"
    POP = "POP"
    BOOL = "BOOL"
    ADD = "ADD"
    SUB = "SUB"
    MUL = "MUL"
    DIV = "DIV"
    REM = "REM"
    NEG = "NEG"
    SWAP = "SWAP"
    QUIT = "QUIT"
    ERROR = "ERROR"
    AND = "AND"
    OR = "OR"
    NOT = "NOT"
    EQUAL = "EQUAL"
    LESS = "LESS"
    BIND = "BIND"
    IF = "IF"
    LET = "LET"
    END = "END"
    FUN = "FUN"
    FUNEND = "FUNEND"
    CALL = "CALL"
    RETURN = "RETURN"
    INOUT = "INOUT"


# extracts file to a stripped list
def extract(text_file):
    file = open(text_file, 'r')
    word = [word.rstrip() for word in file]
    file.close()
    return word


def is_func(line):
    if line[:4] == "fun " and len(line) > 4:
        p = line[4:]
        if p.count(' ') != 1:
            return False
        else:

            f = p.split()
            arg = f.pop()
            fname = f.pop()

            if fname == arg:
                return False
            elif fname[0].isalpha() and arg[0].isalpha() and fname[0:].isalnum() and arg[0:].isalnum():
                return True
            else:
                return False
    else:
        return False


def get_fname_and_arg(line):
    func = line[4:]
    f = func.split()
    arg = f.pop()
    fname = f.pop()
    return fname, arg


def is_in_out(line):
    if line[:9] == "inOutFun " and len(line) > 9:
        p = line[9:]
        if p.count(' ') != 1:
            return False
        else:
            f = p.split()
            arg = f.pop()
            fname = f.pop()

            if fname == arg:
                return False
            elif fname[0].isalpha() and arg[0].isalpha() and fname[0:].isalnum() and arg[0:].isalnum():
                return True
            else:
                return False
    else:
        return False


def get_in_out_params(line):
    func = line[9:]
    f = func.split()
    arg = f.pop()
    fname = f.pop()
    return fname, arg


def is_push(line):
    if line[:5] == 'push ':
        return True
    else:
        return False


def get_push(line, stack):
    if line.startswith("\"") and line.endswith("\""):
        return line
    elif (line.startswith('-') and line[1:].isdigit()) or line[0:].isdigit():
        return int(line)
    elif line in stack.local_func:
        return stack.local_func.get(line)
    elif line in stack.local_var:
        return stack.local_var.get(line)
    elif line[0].isalpha() and line[0:].isalnum():
        return Name(line, None)
    else:
        return ":error:"


def is_int(line):
    if line.startswith('-') and line[1:].isdigit():
        return True
    elif line.isdigit():
        return True
    else:
        return False


def toBool(line):
    if line == ":true:":
        return True
    elif line == ":false:":
        return False
    else:
        return ":error:"


def getCommand(s):
    if is_push(s):
        return Command.PUSH
    elif is_func(s):
        return Command.FUN
    elif is_in_out(s):
        return Command.INOUT
    elif s == "pop":
        return Command.POP
    elif s == "add":
        return Command.ADD
    elif s == "mul":
        return Command.MUL
    elif s == "sub":
        return Command.SUB
    elif s == "div":
        return Command.DIV
    elif s == "rem":
        return Command.REM
    elif s == "neg":
        return Command.NEG
    elif s == "swap":
        return Command.SWAP
    elif s == "quit":
        return Command.QUIT
    elif s == ":true:":
        return Command.BOOL
    elif s == ":false:":
        return Command.BOOL
    elif s == "and":
        return Command.AND
    elif s == "or":
        return Command.OR
    elif s == "not":
        return Command.NOT
    elif s == "equal":
        return Command.EQUAL
    elif s == "lessThan":
        return Command.LESS
    elif s == "bind":
        return Command.BIND
    elif s == "if":
        return Command.IF
    elif s == "let":
        return Command.LET
    elif s == "end":
        return Command.END
    elif s == ":error:":
        return Command.ERROR
    elif s == "funEnd":
        return Command.FUNEND
    elif s == "call":
        return Command.CALL
    elif s == "return":
        return Command.RETURN
    else:
        return Command.ERROR


# y is the top elem and x is the bottom
def arithmetic(cmd, y, x):
    def type_check(a, b):
        if type(a) == int and type(b) == int:
            return True
        elif type(a) == int and type(b) == Name:
            if type(b.get_val()) == int:
                return True
            else:
                return False
        elif type(a) == Name and type(b) == int:
            if type(a.get_val()) == int:
                return True
            else:
                return False
        elif type(a) == Name and type(b) == Name:
            if type(a.get_val()) == int and type(b.get_val()) == int:
                return True
            else:
                return False
        else:
            return False

    if cmd == Command.NEG:
        if type(y) == int:
            return -(y)
        elif type(y) == Name and type(y.get_val()) == int:
            return -(y.get_val())
        else:
            return ":error:"
    elif type_check(x, y) is False:
        return ":error:"
    else:
        if cmd == Command.ADD:
            if type(x) == int and type(y) == int:
                return x + y
            elif type(x) == int and (type(y) == Name and type(y.get_val()) == int):
                return x + y.get_val()
            elif (type(x) == Name and type(x.get_val()) == int) and type(y) == int:
                return x.get_val() + y
            elif (type(x) == Name and type(x.get_val()) == int) and (type(y) == Name and type(y.get_val()) == int):
                return x.get_val() + y.get_val()
            else:
                return ":error:"
        elif cmd == Command.SUB:
            if type(x) == int and type(y) == int:
                return x - y
            elif type(x) == int and (type(y) == Name and type(y.get_val()) == int):
                return x - y.get_val()
            elif (type(x) == Name and type(x.get_val()) == int) and type(y) == int:
                return x.get_val() - y
            elif (type(x) == Name and type(x.get_val()) == int) and (type(y) == Name and type(y.get_val()) == int):
                return x.get_val() - y.get_val()
            else:
                return ":error:"
        elif cmd == Command.MUL:
            if type(x) == int and type(y) == int:
                return x * y
            elif type(x) == int and (type(y) == Name and type(y.get_val()) == int):
                return x * y.get_val()
            elif (type(x) == Name and type(x.get_val()) == int) and type(y) == int:
                return x.get_val() * y
            elif (type(x) == Name and type(x.get_val()) == int) and (type(y) == Name and type(y.get_val()) == int):
                return x.get_val() * y.get_val()
            else:
                return ":error:"
        elif cmd == Command.DIV:
            if type(x) == int and type(y) == int:
                if y == 0:
                    return ":error:"
                else:
                    return x // y
            elif type(x) == int and (type(y) == Name and type(y.get_val()) == int):
                if y.get_val() == 0:
                    return ":error:"
                else:
                    return x // y.get_val()
            elif (type(x) == Name and type(x.get_val()) == int) and type(y) == int:
                if y == 0:
                    return ":error:"
                else:
                    return x // y
            elif (type(x) == Name and type(x.get_val()) == int) and (type(y) == Name and type(y.get_val()) == int):
                if y.get_val() == 0:
                    return ":error:"
                else:
                    return x.get_val() // y.get_val()
            else:
                return ":error:"
        elif cmd == Command.REM:
            if type(x) == int and type(y) == int:
                if y == 0:
                    return ":error:"
                else:
                    return x % y
            elif type(x) == int and (type(y) == Name and type(y.get_val()) == int):
                if y.get_val() == 0:
                    return ":error:"
                else:
                    return x % y.get_val()
            elif (type(x) == Name and type(x.get_val()) == int) and type(y) == int:
                if y == 0:
                    return ":error:"
                else:
                    return x % y
            elif (type(x) == Name and type(x.get_val()) == int) and (type(y) == Name and type(y.get_val()) == int):
                if y.get_val() == 0:
                    return ":error:"
                else:
                    return x % y.get_val()
            else:
                return ":error:"
        else:
            return ":error:"


def logic(cmd, z, y, x, ):
    if cmd == Command.NOT:
        if type(y) == bool:
            if y is False:
                return True
            else:
                return False
        elif type(y) == Name and type(y.get_val()) == bool:
            if y is False:
                return True
            else:
                return False
        else:
            return ":error:"
    elif cmd == Command.IF:
        if type(z) == bool:
            if z is True:
                return x
            else:
                return y
        elif type(z) == Name and type(z.get_val()) == bool:
            if z.get_val() is True:
                return x
            else:
                return y
        else:
            return ":error:"
    else:
        if cmd == Command.AND:
            if type(x) == bool and type(y) == bool:
                return x and y
            elif type(x) == bool and (type(y) == Name and type(y.get_val()) == bool):
                return x and y.get_val()
            elif (type(x) == Name and type(x.get_val()) == bool) and type(y) == bool:
                return x.get_val() and y
            elif (type(x) == Name and type(x.get_val()) == bool) and (type(y) == Name and type(y.get_val()) == bool):
                return x.get_val() and y.get_val()
            else:
                return ":error:"
        elif cmd == Command.OR:
            if type(x) == bool and type(y) == bool:
                return x or y
            elif type(x) == bool and (type(y) == Name and type(y.get_val()) == bool):
                return x or y.get_val()
            elif (type(x) == Name and type(x.get_val()) == bool) and type(y) == bool:
                return x.get_val() or y
            elif (type(x) == Name and type(x.get_val()) == bool) and (type(y) == Name and type(y.get_val()) == bool):
                return x.get_val() or y.get_val()
            else:
                return ":error:"
        elif cmd == Command.EQUAL:
            if type(x) == int and type(y) == int:
                return x == y
            elif type(x) == int and (type(y) == Name and type(y.get_val()) == int):
                return x == y.get_val()
            elif (type(x) == Name and type(x.get_val()) == int) and type(y) == int:
                return x.get_val() == y
            elif (type(x) == Name and type(x.get_val()) == int) and (type(y) == Name and type(y.get_val()) == int):
                return x.get_val() == y.get_val()
            else:
                return ":error:"
        elif cmd == Command.LESS:
            if type(x) == int and type(y) == int:
                return x < y
            elif type(x) == int and (type(y) == Name and type(y.get_val()) == int):
                return x < y.get_val()
            elif (type(x) == Name and type(x.get_val()) == int) and type(y) == int:
                return x.get_val() < y
            elif (type(x) == Name and type(x.get_val()) == int) and (type(y) == Name and type(y.get_val()) == int):
                return x.get_val() < y.get_val()
            else:
                return ":error:"
        else:
            return ":error:"


class Stack:
    def __init__(self):
        self.items = []  # actual stack
        self.local_var = dict()
        self.local_func = dict()

    def push(self, item):
        if type(item) == Name:
            key = item.get_name()
            if key in self.local_var:
                self.items.append(self.local_var.get(key))
            else:
                self.local_var.update({key: item})
                self.items.append(item)
        else:
            self.items.append(item)

    def pop(self):
        if self.len() == 0:
            self.push(":error:")
        else:
            return self.items.pop()

    def math(self, cmd):
        if self.len() >= 1 and cmd == Command.NEG:
            y = self.pop()
            z = arithmetic(cmd, y, 0)
            if z == ":error:":
                self.push(y)
                self.push(z)
            else:
                self.push(z)
        elif self.len() < 2:
            self.push(":error:")
        else:
            y = self.pop()
            x = self.pop()
            z = arithmetic(cmd, y, x)
            if z == ":error:":
                self.push(x)
                self.push(y)
                self.push(z)
            else:
                self.push(z)

    def logical(self, cmd):
        if self.len() >= 1 and cmd == Command.NOT:
            b = self.pop()
            c = logic(cmd, None, b, None)
            if c == ":error:":
                self.push(b)
                self.push(c)
            else:
                self.push(c)
        elif self.len() >= 2 and cmd != Command.IF:
            y = self.pop()
            x = self.pop()
            w = logic(cmd, None, y, x)
            if w == ":error:":
                self.push(x)
                self.push(y)
                self.push(w)
            else:
                self.push(w)
        elif self.len() >= 3 and cmd == Command.IF:
            x = self.pop()
            y = self.pop()
            z = self.pop()
            w = logic(cmd, z, y, x)
            if w == ":error:":
                self.push(z)
                self.push(y)
                self.push(x)
                self.push(w)
            else:
                self.push(w)
        else:
            self.push(":error:")

    def swap(self):
        if self.len() < 2:
            self.push(":error:")
        else:
            x = self.pop()
            y = self.pop()
            self.push(x)
            self.push(y)

    def bind(self):
        if self.len() < 2:
            self.push(":error:")
            return ":error:"
        else:
            v = self.pop()
            n = self.pop()
            if type(n) == Name:
                if v == ":error:" or (type(v) == Name and v.get_val() is None):
                    self.push(n)
                    self.push(v)
                    self.push(":error:")
                    return ":error:"
                else:
                    if type(v) == Name and v.get_val() is not None:
                        key = n.get_name()
                        alias = n.get_alias()
                        n = Name(key, v.get_val())
                        n.set_alias(alias)
                        self.local_var.update({key: n})  # updates var list
                        self.push(":unit:")
                        return n
                    elif v == ":unit:":
                        key = n.get_name()
                        alias = n.get_alias()
                        n = Name(key, v)
                        n.set_alias(alias)
                        self.local_var.update({key: n})  # updates var list
                        self.push(":unit:")
                        return n
                    else:
                        key = n.get_name()
                        alias = n.get_alias()
                        n = Name(key, v)
                        n.set_alias(alias)
                        self.local_var.update({key: n})  # updates var list
                        self.push(":unit:")
                        return n
            else:
                self.push(n)
                self.push(v)
                self.push(":error:")
                return ":error:"

    def len(self):
        return len(self.items)

    def add_var(self, expr):
        if expr not in self.local_var:
            self.local_var.update({expr.get_name: expr})

    def get_var(self, expr):
        if expr in self.local_var:
            self.local_var.get(expr.get_name)

    def show_vars(self):
        for key in self.local_var:
            var = self.local_var.get(key)
            if type(var) == Name:
                print("Var: %s, Value: %s " % (key, var.get_val()))

    def createNewFunc(self, fname, arg):
        func = Func(fname, arg, self.local_var, self.local_func)
        func.fill_parent_vars()
        func.fill_parent_funcs()
        self.local_func.update({fname: func})

    def createNewInOut(self, fname, arg):
        if fname not in self.local_func:
            io = InOut(fname, arg, self.local_var, self.local_func)
            io.fill_parent_vars()
            io.fill_parent_funcs()
            self.local_func.update({fname: io})

    def fill_func(self, key, line):
        func = self.local_func.get(key)
        func.copy_instructions(line)

    def get_func(self):
        return self.local_func

    def prints(self):
        return [item for item in self.items]


class Let(Stack):
    def __init__(self, vars_dict, func_dict):
        super().__init__()
        self.parent_vars = vars_dict
        self.parent_funcs = func_dict

    def push(self, item):
        if type(item) == Name:
            key = item.get_name()
            if key in self.parent_vars:
                self.items.append(self.parent_vars.get(key))
            elif key in self.local_var:
                self.items.append(self.local_var.get(key))
            elif key in self.parent_funcs:
                self.items.append(self.parent_funcs.get(key))
            elif key in self.local_func:
                self.items.append(self.local_func.get(key))
            else:
                self.local_var.update({key: item})
                self.items.append(item)
        elif type(item) == Func or type(item) == InOut:
            key = item.get_fname()
            if key in self.parent_funcs:
                self.items.append(self.parent_funcs.get(key))
            elif key in self.local_func:
                self.items.append(self.local_func.get(key))
            else:
                self.local_func.update({key: item})
                self.items.append(item)
        else:
            self.items.append(item)

    def bind(self):
        if self.len() < 2:
            self.push(":error:")
            return ":error:"
        else:
            v = self.pop()
            n = self.pop()
            if type(n) == Name:
                if v == ":error:" or (type(v) == Name and v.get_val() is None):
                    self.push(n)
                    self.push(v)
                    self.push(":error:")
                    return ":error:"
                else:
                    if type(v) == Name and v.get_val() is not None:  # updates a name to a name
                        key = n.get_name()
                        n = Name(key, v.get_val())
                        self.local_var.update({key: n})  # updates var list
                        self.push(":unit:")
                        return n
                    elif v == ":unit:":  # updates name to :unit:
                        key = n.get_name()
                        n = Name(key, v)
                        self.local_var.update({key: n})  # updates var list
                        self.push(":unit:")
                        return n
                    else:
                        key = n.get_name()
                        if key in self.parent_vars:
                            n = Name(key, v)
                            self.parent_vars.update({key: n})
                            self.push(":unit:")
                            return n
                        else:
                            n = Name(key, v)
                            self.local_var.update({key: n})  # updates var list
                            self.push(":unit:")
                            return n
            else:
                self.push(n)
                self.push(v)
                self.push(":error:")
                return ":error:"

    def var_to_child(self):
        return {**self.parent_vars, **self.local_var}

    def func_to_child(self):
        return {**self.parent_funcs, **self.local_func}

    def createNewFunc(self, fname, arg):
        func = Func(fname, arg, self.var_to_child(), self.func_to_child())
        func.fill_parent_vars()
        func.fill_parent_funcs()
        self.local_func.update({fname: func})

    def createNewInOut(self, fname, arg):
        io = InOut(fname, arg, self.var_to_child(), self.func_to_child())
        io.fill_parent_vars()
        io.fill_parent_funcs()
        self.local_func.update({fname: io})

    def show_inherit_vars(self):
        for key in self.parent_vars:
            var = self.parent_vars.get(key)
            if type(var) == Name:
                print("Inherit Var: %s, Value: %s " % (key, var.get_val()))


class Environment:
    def __init__(self):
        self.stacks = []  # list of stacks
        self.vars = dict()
        self.funcs = dict()

    def createNewStack(self):
        s = Stack()
        if len(self.vars) > 0:
            for key, value in self.vars.items():
                s.local_var.update({key: value})
        if len(self.funcs) > 0:
            for key, value in self.funcs.items():
                s.local_func.update({key: value})
        self.stacks.append(s)

    def createLet(self):
        if type(self.stacks[-1]) == Stack:
            self.stacks.append(Let(self.stacks[-1].local_var, self.stacks[-1].local_func))  # adds to the end
        elif type(self.stacks[-1]) == Let:
            self.stacks.append(Let(self.stacks[-1].var_to_child(), self.stacks[-1].func_to_child()))
        return self.stacks[-1]  # gets the latest result

    def createNewFunc(self, fname, arg):
        if type(self.stacks[-1]) == Stack:
            func = Func(fname, arg, self.stacks[-1].local_var, self.stacks[-1].local_func)
            # func.fill_parent_vars()
            self.stacks.append(func)  # adds to the end
        elif type(self.stacks[-1]) == Let:
            func = Func(fname, arg, self.stacks[-1].local_var, self.stacks[-1].local_func)
            # func.fill_parent_vars()
            self.stacks.append(func)
        return self.stacks[-1]  # gets the latest result

    def createNewInOut(self, fname, arg):
        if type(self.stacks[-1]) == Stack:
            io = InOut(fname, arg, self.stacks[-1].local_var, self.stacks[-1].local_func)
            # func.fill_parent_vars()
            self.stacks.append(io)  # adds to the end
        elif type(self.stacks[-1]) == Let:
            io = InOut(fname, arg, self.stacks[-1].local_var, self.stacks[-1].local_func)
            # func.fill_parent_vars()
            self.stacks.append(io)
        return self.stacks[-1]  # gets the latest result

    def stream(self, instructions):

        self.createNewStack()

        stack = self.stacks[-1]  # initial

        fill = False  # fill function with strings
        func_name = ""

        for line in instructions:
            if fill:
                if line != "funEnd":
                    stack.fill_func(func_name, line)
                else:
                    fill = False
                    func_name = ""
                    stack.push(":unit:")
            else:
                cmd = getCommand(line)

                if cmd == Command.PUSH:
                    expr = get_push(line[5:], stack)
                    if type(expr) == Name:
                        stack.push(expr)
                    elif type(expr) == Func:
                        stack.push(expr)
                    else:
                        stack.push(expr)
                elif cmd == Command.FUN:
                    if is_func(line):
                        fname, arg = get_fname_and_arg(line)
                        stack.createNewFunc(fname, arg)
                        fill = True
                        func_name = fname
                    else:
                        stack.push(":error:")
                elif cmd == Command.INOUT:
                    if is_in_out(line):
                        fname, arg = get_in_out_params(line)
                        stack.createNewInOut(fname, arg)
                        fill = True
                        func_name = fname
                elif cmd == Command.POP:
                    stack.pop()
                elif cmd == Command.BOOL:
                    expr = toBool(line)
                    stack.push(expr)
                elif cmd == Command.ADD:
                    stack.math(cmd)
                elif cmd == Command.SUB:
                    stack.math(cmd)
                elif cmd == Command.MUL:
                    stack.math(cmd)
                elif cmd == Command.DIV:
                    stack.math(cmd)
                elif cmd == Command.REM:
                    stack.math(cmd)
                elif cmd == Command.NEG:
                    stack.math(cmd)
                elif cmd == Command.SWAP:
                    stack.swap()
                elif cmd == Command.QUIT:
                    return stack.prints()
                elif cmd == Command.ERROR:
                    stack.push(":error:")
                elif cmd == Command.AND:
                    stack.logical(cmd)
                elif cmd == Command.OR:
                    stack.logical(cmd)
                elif cmd == Command.NOT:
                    stack.logical(cmd)
                elif cmd == Command.EQUAL:
                    stack.logical(cmd)
                elif cmd == Command.LESS:
                    stack.logical(cmd)
                elif cmd == Command.BIND:
                    result = stack.bind()
                    if result != ":error:":
                        if type(self) == InOut:
                            key = result.get_name()
                            if key in self.vars:
                                self.vars.update({key: result})
                        for block in self.stacks:
                            key = result.get_name()
                            if type(block) == Stack:
                                if key in block.local_var:
                                    block.local_var.update({key: result})
                elif cmd == Command.IF:
                    stack.logical(cmd)
                elif cmd == Command.LET:
                    stack = self.createLet()
                elif cmd == Command.END:
                    if len(stack.items) > 0:
                        last = stack.pop()
                        if len(self.stacks) > 1:
                            self.stacks.pop()
                            stack = self.stacks[-1]
                            stack.push(last)
                        else:
                            stack.push(":error:")
                    else:
                        self.stacks.pop()
                        stack = self.stacks[-1]
                elif cmd == Command.CALL:
                    if stack.len() < 2:
                        stack.push(":error:")
                    else:
                        func = stack.pop()
                        arg = stack.pop()
                        if type(func) == Func and arg != ":error:":
                            look_up = func.get_fname()
                            if look_up in stack.local_func:
                                if type(arg) == Name:
                                    if arg.get_name() in stack.local_var and arg.get_val() != None:
                                        func.set_arg_value(arg)
                                        result = func.call_function()
                                        if result is not None:
                                            stack.push(result)
                                    else:
                                        stack.push(arg)
                                        stack.push(func)
                                        stack.push(":error:")
                                else:
                                    func.set_arg_value(arg)
                                    result = func.call_function()
                                    if result is not None:
                                        stack.push(result)
                            else:
                                stack.push(arg)
                                stack.push(func)
                                stack.push(":error:")
                        elif type(func) == InOut and arg != ":error:":
                            look_up = func.get_fname()
                            if look_up in stack.local_func:
                                if type(arg) == Name:
                                    if arg.get_name() in stack.local_var and arg.get_val() != None:
                                        linked_arg = func.set_arg_value(arg)
                                        result, do_push = func.call_function(linked_arg)
                                        if do_push is True:
                                            if type(result) == Name:
                                                stack.push(result.get_val())
                                            else:
                                                stack.push(result)
                                        for block in self.stacks:
                                            if type(result) == Name:
                                                key = result.get_name()
                                                if type(block) == Let:
                                                    block.parent_vars.update({key: result})
                                                    block.local_var.update({key: result})
                                                elif type(block) == Stack:
                                                    if key in block.local_var:
                                                        block.local_var.update({key: result})
                                            else:
                                                if type(block) == Let:
                                                    if key in block.parent_vars:
                                                        v = Name(key, result)
                                                        block.parent_vars.update({key: v})
                                                    if key in block.local_var:
                                                        v = Name(key, result)
                                                        block.local_var.update({key: v})
                                                elif type(block) == Stack:
                                                    if key in block.local_var:
                                                        v = Name(key, result)
                                                        block.local_var.update({key: v})


                                    else:
                                        stack.push(arg)
                                        stack.push(func)
                                        stack.push(":error:")
                                else:
                                    func.set_arg_value(arg)
                                    result = func.call_function()
                                    if result is not None:
                                        stack.push(result)
                            elif type(stack) == Let:
                                pass
                            else:
                                stack.push(arg)
                                stack.push(func)
                                stack.push(":error:")
                        elif type(func) == Name and arg != ":error:":  # function as argument!
                            fun = func.get_val()
                            if type(fun) == Func:
                                look_up = fun.get_fname()
                                if look_up in stack.local_func:
                                    if type(arg) == Name:
                                        if arg.get_name() in stack.local_var and arg.get_val() != None:
                                            fun.set_arg_value(arg)
                                            result = fun.call_function()
                                            if result is not None:
                                                stack.push(result)
                                        else:
                                            stack.push(arg)
                                            stack.push(fun)
                                            stack.push(":error:")
                                    else:
                                        fun.set_arg_value(arg)
                                        result = fun.call_function()
                                        if result is not None:
                                            stack.push(result)
                                else:
                                    stack.push(arg)
                                    stack.push(fun)
                                    stack.push(":error:")
                                    # perhaps add InOut function
                            else:
                                stack.push(arg)
                                stack.push(func)
                                stack.push(":error:")
                        else:
                            stack.push(arg)
                            stack.push(func)
                            stack.push(":error:")
                elif cmd == Command.RETURN:
                    return stack.pop()
                else:
                    return ":error:"


class Func(Environment):
    def __init__(self, fname, arg, vars_dict, func_dict):
        super().__init__()
        self.fname = fname
        self.arg = arg
        self.parent_vars = vars_dict
        self.parent_funcs = func_dict
        self.instructions = []
        self.return_called = False

    def createNewStack(self):
        s = Stack()
        if len(self.vars) > 0:
            for key, value in self.vars.items():
                s.local_var.update({key: value})
        if len(self.funcs) > 0:
            for key, value in self.parent_funcs.items():
                s.local_func.update({key: value})
        self.stacks.append(s)

    def copy_instructions(self, line):
        self.instructions.append(line)

    def get_fname(self):
        return self.fname

    def get_arg_name(self):
        return self.arg

    def set_arg_value(self, item):
        if type(item) == Name:
            var = Name(self.arg, item.get_val())
            self.vars.update({self.arg: var})
        else:
            var = Name(self.arg, item)
            self.vars.update({self.arg: var})

    def fill_parent_vars(self):
        for key, val in self.parent_vars.items():
            self.vars.update({key: val})

    def fill_parent_funcs(self):
        for key, val in self.parent_funcs.items():
            self.funcs.update({key: val})

    def call_function(self):
        result = self.stream(self.instructions)
        if type(result) == Name:
            return result.get_val()
        else:
            return result


class InOut(Environment):
    def __init__(self, fname, arg, vars_dict, func_dict):
        super().__init__()
        self.fname = fname
        self.arg = arg
        self.parent_vars = vars_dict
        self.parent_funcs = func_dict
        self.instructions = []

    def createNewStack(self):
        s = Stack()
        if len(self.vars) > 0:
            for key, value in self.vars.items():
                s.local_var.update({key: value})
        if len(self.funcs) > 0:
            for key, value in self.parent_funcs.items():
                s.local_func.update({key: value})
        self.stacks.append(s)

    def copy_instructions(self, line):
        self.instructions.append(line)

    def get_fname(self):
        return self.fname

    def get_arg_name(self):
        return self.arg

    def set_arg_value(self, item):
        if type(item) == Name:
            var = Name(self.arg, item.get_val())
            var.set_alias(item.get_name())
            self.vars.update({self.arg: var})
            return var
        else:
            var = Name(self.arg, item)
            self.vars.update({self.arg: var})
            return var

    def fill_parent_vars(self):
        for key, val in self.parent_vars.items():
            self.vars.update({key: val})

    def fill_parent_funcs(self):
        for key, val in self.parent_funcs.items():
            self.funcs.update({key: val})

    def call_function(self, arg):
        return_called = self.stream(self.instructions)
        if return_called is None:
            reference = arg.get_alias()
            for key, val in self.vars.items():
                var = self.vars.get(key)
                if var.get_alias() == reference:
                    if var.get_val() != arg.get_val():
                        name = var.get_alias()
                        n = Name(name, var.get_val())
                        return n, False
        else:
            reference = arg.get_alias()
            for key, val in self.vars.items():
                var = self.vars.get(key)
                if var.get_alias() == reference:
                    if var.get_val() != arg.get_val():
                        name = var.get_alias()
                        n = Name(name, var.get_val())
                        return n, True


def printStack(results, output):
    with open(output, 'w') as file:
        for item in results[::-1]:
            if type(item) == bool:
                if item == True:
                    file.write("%s\n" % ":true:")
                elif item == False:
                    file.write("%s\n" % ":false:")
            elif type(item) == int:
                file.write("%s\n" % str(item))
            elif type(item) == Name:
                file.write("%s\n" % item.get_name())
            elif type(item) == Func:
                file.write("%s\n" % item.get_fname())
            elif item == ":error:":
                file.write("%s\n" % item)
            elif item == ":unit:":
                file.write("%s\n" % item)
            elif type(item) == str:
                file.write("%s\n" % item.strip("\""))
    file.close()


def interpreter(input, output):
    words = extract(input)
    e = Environment()
    e.stream(words)
    pt1 = e.stacks.pop()
    printStack(pt1.prints(), output)
