from interpreter.commands import Command



class Item:
    """Stores values to be put on the Stack."""
    def __init__(self, name: str, value):
        self.name = name  # variable name or function name
        self.value = value  # any type
        self.alias = ""

    def __add__(self, other):
        if isinstance(other, Item):
            return self.value + other.value
        else:
            return self.value + other

    def __radd__(self, other):
        return other + self.value

    def __sub__(self, other):
        if isinstance(other, Item):
            return self.value - other.value
        else:
            return self.value - other

    def __rsub__(self, other):
        return other - self.value

    def __mul__(self, other):
        if isinstance(other, Item):
            return self.value * other.value
        else:
            return self.value * other

    def __rmul__(self, other):
        return other * self.value

    def __floordiv__(self, other):
        if isinstance(other, Item):
            return self.value // other.value
        else:
            return self.value // other

    def __rfloordiv__(self, other):
        return other // self.value

    def __mod__(self, other):
        if isinstance(other, Item):
            return self.value % other.value
        else:
            return self.value % other

    def __rmod__(self, other):
        return other % self.value

    def __neg__(self):
        return -self.value

    def __bool__(self):
        return self.value

    def __and__(self, other):
        if isinstance(other, Item):
            return self.value & other.value
        else:
            return self.value & other

    def __rand__(self, other):
        return other & self.value

    def __or__(self, other):
        if isinstance(other, Item):
            return self.value | other.value
        else:
            return self.value | other

    def __ror__(self, other):
        return other | self.value

    def __eq__(self, other):
        if isinstance(other, Item):
            return self.value == other.value
        else:
            return self.value == other

    def __req__(self, other):
        return other == self.value

    def __lt__(self, other):
        if isinstance(other, Item):
            return self.value < other.value
        else:
            return self.value < other

    def __rlt__(self, other):
        return other < self.value



class Stack:
    """Represents and execution stack."""
    def __init__(self):
        self.items = []  # actual stack
        self.local_var = dict()  # {key: str => value: Item}
        self.local_func = dict()  # {key: str => value: Item}

    def __len__(self) -> int:
        return len(self.items)

    def __str__(self) -> str:
        return str(self.items)

    def push(self, item: Item) -> None:
        """Pushes an Item or some value(i.e. 1, 2, ':error:') to the Stack.

        ex. push variable_name
            push 1
        """
        if isinstance(item, Item):
            key = item.name
            if key in self.local_var:
                # add existing variable element to the stack
                variable = self.local_var.get(key)
                self.items.append(variable)
            else:
                # save new variable element then add it to the stack
                self.local_var.update({key: item})
                self.items.append(item)
        else:
            self.items.append(item)

    def pop(self) -> Item:
        """Pops an item off of the Stack.

        Returns:
            :return: Item or value off of the stack.
                     pushes ':error:' on to the stack if stack is empty.
        """
        if len(self.items) == 0:
            self.push(":error:")
        else:
            return self.items.pop()

    def same_type(self, a, b) -> bool:
        """Checks if the types are the same.

        Returns:
            :return: True, types or Item values are the same.
                     False, types or Item values do not match.
        """
        if isinstance(a, Item) and isinstance(b, Item):
            return isinstance(a.value, type(b.value)) == isinstance(b.value, type(a.value))
        elif isinstance(a, Item) and not isinstance(b, Item):
            return isinstance(a.value, type(b))
        elif not isinstance(a, Item) and isinstance(b, Item):
            return isinstance(b.value, type(a))
        else:
            return isinstance(a, type(b))

    def match_type(self, t: type, *args) -> bool:
        """Checks if the types are the same.

        Returns:
            :return: True, types or Item values are the same.
                     False, types or Item values do not match.
        """
        for arg in args:
            if isinstance(arg, Item):
                if not isinstance(arg.value, t):
                    return False
            else:
                if not isinstance(arg, t):
                    return False
        return True

    def arithmetic(self, cmd: Command, y: int, x: int) -> int:
        """Conducts mathematical operations relative to items on stack.

                        visual example:
              |   inst.     stack    assign    result
              |
            x |  push 1      sub     -
            y |  push 2  =>  2   =>  y=2 =>  x-y = -1
          cmd |  sub         1       x=1

                      error example:
              |   inst.     stack    assign         result
              |
            x |  push 1      div     /
            y |  push 0  =>  0   =>  y=0 =>     x / y = ':error:'
          cmd |  div         1       x=1

        Args:
            :params y: first item popped off the top of the stack.
                    x: second item popped off stack.

        Returns:
            :return: int: result of mathematical expression.
                     str: ':error:' if errors occurred.
        """
        if isinstance(y, int) or isinstance(x, int) or isinstance(y, Item) or isinstance(x, Item):
            if self.same_type(x, y) is False:
                return ":error:"
            elif cmd == Command.NEG:
                return -y
            elif cmd == Command.ADD:
                return x + y
            elif cmd == Command.SUB:
                return x - y
            elif cmd == Command.MUL:
                return x * y
            elif cmd == Command.DIV:
                if (isinstance(y, Item) and y.value == 0) or y == 0:
                    return ':error:'
                else:
                    return x // y
            elif cmd == Command.REM:
                if (isinstance(y, Item) and y.value == 0) or y == 0:
                    return ":error:"
                else:
                    return x % y
            else:
                return ":error:"
        else:
            return ':error:'


    def math(self, cmd: Command) -> None:
        """Calls mathematical operations relative to items on stack and
           pushes results to the top of the stack.

                        visual example:
              |   inst.     stack    assign    eval.       stack
              |
            x |  push 1      sub     -
            y |  push 2  =>  2   =>  y=2 =>  x-y = -1   =>
          cmd |  sub         1       x=1                    -1

                        error example:
              |   inst.     stack    assign    eval.            stack
              |
            x |  push 1      div     /                          ':error:'
            y |  push 0  =>  0   =>  y=0 =>  x / y = err   =>   0
          cmd |  div         1       x=1                        1

        y: first item popped off the top of the stack.
        x: second item popped off the top of the stack.

        Arg:
            :param cmd: mathematical operation.
        """
        if len(self.items) >= 1 and cmd == Command.NEG:
            y = self.pop()
            z = self.arithmetic(cmd, y, 0)  # ignore second arg
            if z == ":error:":
                # revert for error
                self.push(y)
                self.push(z)
            else:
                # result
                self.push(z)
        elif len(self.items) < 2:
            # not enough items on stack for mathematical evaluation.
            self.push(":error:")
        else:
            y = self.pop()
            x = self.pop()
            z = self.arithmetic(cmd, y, x)
            if z == ":error:":
                # revert for error
                self.push(x)
                self.push(y)
                self.push(z)
            else:
                # result
                self.push(z)

    def logic(self, cmd, z, y, x) -> bool:
        # not sure if language allows for numerical boolean values!
        if cmd == Command.NOT:
            if self.match_type(bool,y):
                return not y  # might have to return Item as well.
            else:
                return ":error:"
        elif cmd == Command.IF:
            if type(z) == bool:
                if z is True:
                    return x
                else:
                    return y
            elif isinstance(z, Item):
                if type(z.value) == bool and z.value is True:
                    return x
                else:
                    return y
            else:
                return ":error:"
        elif cmd == Command.AND:
            if self.match_type(bool,x,y):
                return x & y
            else:
                return ":error:"
        elif cmd == Command.OR:
            if self.match_type(bool,x,y):
                return x | y
            else:
                return ":error:"
        elif cmd == Command.EQUAL:
            if self.match_type(int,x,y) and not self.match_type(bool,x,y):
                return x == y
            else:
                return ":error:"
        elif cmd == Command.LESS:
            if self.match_type(int,x,y) and not self.match_type(bool,x,y):
                return x < y
            else:
                return ":error:"
        else:
            return ":error:"

    def logical(self, cmd: Command) -> None:
        """Performs logical operations on the stack."""
        if len(self.items) >= 1 and cmd == Command.NOT:
            x = self.pop()
            y = self.logic(cmd, None, x, None)
            if y == ":error:":
                self.push(x)
                self.push(y)
            else:
                self.push(y)
        elif len(self.items) >= 2 and (
        cmd == Command.AND or
         cmd == Command.OR or
          cmd == Command.EQUAL or
           cmd == Command.LESS):
            y = self.pop()
            x = self.pop()
            w = self.logic(cmd, None, y, x)
            if w == ":error:":
                self.push(x)
                self.push(y)
                self.push(w)
            else:
                self.push(w)
        elif len(self.items) >= 3 and cmd == Command.IF:
            x = self.pop()
            y = self.pop()
            z = self.pop()
            w = self.logic(cmd, z, y, x)
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
        """Swaps two items on the Stack."""
        if len(self.items) < 2:
            self.push(":error:")
        else:
            x = self.pop()  # top of stack
            y = self.pop()
            self.push(x)
            self.push(y)  # top of stack

    def bind(self) -> Item:
        """Takes two items off the stack and assigns a variable a value.

        Variable can take any value except:
            ':error:' or another unassigned variable's value: None

        Once successful, function pushes ':unit:' to mark completion on the stack,
        adds/updates the variable to the local_var dict(), and returns the variable.

        Returns:
            :return: ':error:', conflicts or not enough items on stack
                      Item, variable that has been added/updated with new value.
        """
        if len(self.items) < 2:
            self.push(":error:")
            return ":error:"
        else:
            value = self.pop()  # value to be assigned, top of stack
            var = self.pop()  # variable to assign value too
            if not isinstance(var, Item) or value == ":error:" or (
            isinstance(value, Item) and value.value is None):
                # error
                self.push(var)
                self.push(value)
                self.push(":error:")
                return ":error:"
            else:
                key = var.name
                alias = var.alias
                # update var's value
                if isinstance(value, Item) and value.value is not None:
                    var = Item(key, value.value)
                elif value == ':unit:':
                    var = Item(key, ':unit:')
                else:
                    var = Item(key, value)
                var.alias = alias  # reuse same alias
                self.local_var.update({key: var})  # update var list
                self.push(":unit:")
                return var  # could return ':unit:'

    def create_func(self, fname: str, arg: str) -> None:
        """Creates function environment."""
        func = Func(fname, arg, self.local_var, self.local_func)
        func.fill_parent_vars()
        func.fill_parent_funcs()
        self.local_func.update({fname: func})

    def create_io(self, fname: str, arg: str) -> None:
        """Creates InOut function environment."""
        if fname not in self.local_func:
            io = InOut(fname, arg, self.local_var, self.local_func)
            io.fill_parent_vars()
            io.fill_parent_funcs()
            self.local_func.update({fname: io})

    def fill_func(self, key: str, line: str) -> None:
        """Copies instructions to function environment."""
        func = self.local_func.get(key)
        func.copy(line)


class Let(Stack):
    """Small execution stack. Copies vars, funcs, from parent stack to use."""
    def __init__(self, vars_dict, func_dict):
        super().__init__()
        self.parent_vars = vars_dict
        self.parent_funcs = func_dict

    def push(self, item: Item) -> None:
        """Creates new Items on the stack or copies them from parents."""
        if isinstance(item, Item):
            key = item.name
            # add Item to local stack
            if key in self.parent_vars:
                self.items.append(self.parent_vars.get(key))
            elif key in self.parent_funcs:
                self.items.append(self.parent_funcs.get(key))
            elif key in self.local_var:
                self.items.append(self.local_var.get(key))
            elif key in self.local_func:
                self.items.append(self.local_func.get(key))
            else:
                # new Item
                self.local_var.update({key: item})
                self.items.append(item)
        elif isinstance(item, Environment) and type(item) != Environment:
            key = item.fname
            if key in self.parent_funcs:
                self.items.append(self.parent_funcs.get(key))
            elif key in self.local_func:
                self.items.append(self.local_func.get(key))
            else:
                self.local_func.update({key: item})
                self.items.append(item)
        else:
            self.items.append(item)

    def bind(self) -> Item:
        """Assigns a variable to a value."""
        if len(self.items) < 2:
            self.push(":error:")
            return ":error:"
        else:
            value = self.pop()  # value to be assigned, top of stack
            var = self.pop()  # variable to assign value too
            if not isinstance(var, Item) or value == ":error:" or (
            isinstance(value, Item) and value.value is None):
                # error
                self.push(var)
                self.push(value)
                self.push(":error:")
                return ":error:"
            else:
                key = var.name
                if isinstance(value, Item) and value.value is not None:
                    var = Item(key, value.value)
                elif value == ':unit:':
                    var = Item(key, ':unit:')
                else:
                    var = Item(key, value)
                # ignore alias
                if key in self.parent_vars:
                    self.parent_vars.update({key: var})  # update parent var?
                else:
                    self.local_var.update({key: var})  # update local var
                self.push(":unit:")
                return var  # could return ':unit:'

    def var_to_child(self) -> dict:
        """Returns a copy of all variables."""
        return {**self.parent_vars, **self.local_var}

    def func_to_child(self) -> dict:
        """Returns a copy of all functions."""
        return {**self.parent_funcs, **self.local_func}

    def create_func(self, fname: str, arg: str) -> None:
        """Creates local function environment."""
        func = Func(fname, arg, self.var_to_child(), self.func_to_child())
        func.fill_parent_vars()
        func.fill_parent_funcs()
        self.local_func.update({fname: func})

    def create_io(self, fname: str, arg: str) -> None:
        """Creates local InOut function environment."""
        io = InOut(fname, arg, self.var_to_child(), self.func_to_child())
        io.fill_parent_vars()
        io.fill_parent_funcs()
        self.local_func.update({fname: io})



class Environment:
    """Controls the execution stack and creates other stacks for independant evaluations."""
    def __init__(self):
        self.stacks = []  # list of stacks
        self.vars = dict()
        self.funcs = dict()
        self.keywords = {
            'pop': Command.POP,
            'fun': Command.FUN,
            'inout': Command.INOUT,
            'add': Command.ADD,
            'mul': Command.MUL,
            'sub': Command.SUB,
            'div': Command.DIV,
            'rem': Command.REM,
            'neg': Command.NEG,
            'swap': Command.SWAP,
            'quit': Command.QUIT,
            ':true:': Command.BOOL,
            ':false:': Command.BOOL,
            'and': Command.AND,
            'or': Command.OR,
            'not': Command.NOT,
            'equal': Command.EQUAL,
            'lessThan': Command.LESS,
            'bind': Command.BIND,
            'if': Command.IF,
            'let': Command.LET,
            'end': Command.END,
            ':error:': Command.ERROR,
            'funEnd': Command.FUNEND,
            'call': Command.CALL,
            'return': Command.RETURN,
        }

    def __len__(self) -> int:
        return len(self.stacks)

    def __str__(self) -> str:
        return str(self.stacks)

    def create_stack(self) -> None:
        """Creates a stack and adds it to the environment list of stacks."""
        stack = Stack()
        if len(self.vars) > 0:
            for key, value in self.vars.items():
                stack.local_var.update({key: value})  # add existing vars to stack
        if len(self.funcs) > 0:
            for key, value in self.funcs.items():
                stack.local_func.update({key: value})  # add existing funs to stack
        self.stacks.append(stack)  # add stack

    def create_let(self) -> Stack:
        """Creates a let stack and adds it to the environment list of stacks."""
        if len(self.stacks) > 0:
            if type(self.stacks[-1]) == Stack:
                self.stacks.append(Let(self.stacks[-1].local_var, self.stacks[-1].local_func))  # adds to the end
            elif type(self.stacks[-1]) == Let:
                self.stacks.append(Let(self.stacks[-1].var_to_child(), self.stacks[-1].func_to_child()))
        else:
            self.stacks.append(Let(self.vars,self.funcs))  # copy global vars/funcs
        return self.stacks[-1]  # gets the latest result

    def create_func(self, fname: str, arg: str) -> Stack:
        """Creates a function environment and adds it to the environment functions."""
        if len(self.stacks) > 0:
            if type(self.stacks[-1]) == Stack:
                func = Func(fname, arg, self.stacks[-1].local_var, self.stacks[-1].local_func)
                # func.fill_parent_vars()
                self.stacks.append(func)  # adds to the end
            elif type(self.stacks[-1]) == Let:
                func = Func(fname, arg, self.stacks[-1].local_var, self.stacks[-1].local_func)
                # func.fill_parent_vars()
                self.stacks.append(func)
        else:
            self.stacks.append(Func(fname, arg, self.vars, self.funcs)) # copy global vars/funcs
        return self.stacks[-1]  # gets the latest result

    def create_io(self, fname: str, arg: str):
        """Creates a InOut function environment and adds it to the environment functions."""
        if len(self.stacks) > 0:
            if type(self.stacks[-1]) == Stack:
                io = InOut(fname, arg, self.stacks[-1].local_var, self.stacks[-1].local_func)
                # func.fill_parent_vars()
                self.stacks.append(io)  # adds to the end
            elif type(self.stacks[-1]) == Let:
                io = InOut(fname, arg, self.stacks[-1].local_var, self.stacks[-1].local_func)
                # func.fill_parent_vars()
                self.stacks.append(io)
        else:
            self.stacks.append(InOut(fname, arg, self.vars, self.funcs))
        return self.stacks[-1]  # gets the latest result

    def get_push(self, line: str, stack: Stack):
        """Gets value associated with push: value, variable, or function from instructions."""
        if line.startswith("\"") and line.endswith("\""):
            return line
        elif (line.startswith('-') and line[1:].isdigit()) or line[0:].isdigit():
            return int(line)
        elif line in stack.local_func:
            return stack.local_func.get(line)
        elif line in stack.local_var:
            return stack.local_var.get(line)
        elif line[0].isalpha() and line[0:].isalnum():
            return Item(line, None)
        else:
            return ":error:"

    def get_fname_and_arg(self, line: str) -> (str, str):
        """Gets function and function arg associated with 'fun' from instructions."""
        func = line[4:]
        f = func.split()
        arg = f.pop()
        fname = f.pop()
        return fname, arg

    def get_in_out_params(self, line: str):
        """Gets function and function arg associated with 'InOut' from instructions."""
        func = line[9:]
        f = func.split()
        arg = f.pop()
        fname = f.pop()
        return fname, arg

    def is_func(self, line: str) -> bool:
        """Checks if function and function arguments are valid.

        ex. 'fun functionName arg1 arg2 ... argN'

        Arg:
            :param line: str
        Returns:
            :return: True, line is in a valid function format.
                     False, line conflicts with other keywords or identifiers.
        """
        if line[:4] == "fun " and len(line) > 4:
            fn_metadata = line[4:]
            fn = fn_metadata.split()
            if fn and len(fn) > 1:
                fn_items = {}  # save to items to globally perhaps...
                fn_name = fn.pop(0)
                if fn_name[0].isalpha() and fn_name[0:].isalnum() and fn_name not in self.keywords and fn_name not in fn_items:
                    fn_items[fn_name] = fn_name
                else:
                    return False
                fn_args = fn
                for arg in fn_args:
                    if arg[0].isalpha() and arg[0:].isalnum() and arg not in self.keywords and arg not in fn_items:
                        fn_items[arg] = arg
                    else:
                        return False
                # all naming conventions are met and no conflicts or repetition exist.
                return True
            else:
                return False
        else:
            return False

    def is_push(self, line: str) -> bool:
        """Pushes an item to a stack.

        ex. 'push variable'
            'push 1'
            'push functionName'

        Note: only one item can be pushed.

        Arg:
            :param line: str
        Returns:
            :return: True, line is correctly formatted.
                     False, line pushes too many items or none at all.
        """
        if line[:5] == 'push ':
            items = line[5:].split()
            if not items:
                return False
            else:
                return True
        else:
            return False

    def is_int(self, value: str) -> bool:
        """Checks if value is an integer (positive or negative).

        Arg:
            :param value: str
        Returns:
            :return: True, value is an integer.
                     False, value has conflicts, NaN.
        """
        if value.startswith('-') and value[1:].isdigit():
            return True
        elif value.isdigit():
            return True
        else:
            return False


    def is_in_out(self, line: str) -> bool:
        """Checks if InOut function and argument are valid.

        ex. 'inOutFun functionName arg'

        Note: only one argument allowed.

        Arg:
            :param line: str
        Returns:
            :return: True, line is in a valid InOut function format.
                     False, line conflicts with other keywords or identifiers.
        """
        if line[:9] == "inOutFun " and len(line) > 9:
            fn_metadata = line[9:]
            fn = fn_metadata.split()
            if fn and len(fn) > 1:
                fn_arg = fn.pop()
                fn_name = fn.pop()
                if fn_name == fn_arg:
                    return False
                elif fn_name in self.keywords or fn_arg in self.keywords:
                    return False
                elif fn_name[0].isalpha() and fn_arg[0].isalpha() and fn_name[0:].isalnum() and fn_arg[0:].isalnum():
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    def to_bool(self, line: str) -> bool:
        """Converts instruction to boolean value."""
        if line == ":true:":
            return True
        elif line == ":false:":
            return False
        else:
            return ":error:"

    def translate(self, line: str) -> Command:
        """Translates instructions to machine-readable commands.

        Arg:
            :param line: instructions from .txt file
        Returns:
            :return: Command Type
        """
        if self.is_push(line):
            return Command.PUSH
        elif self.is_func(line):
            return Command.FUN
        elif self.is_in_out(line):
            return Command.INOUT
        elif line == "pop":
            return Command.POP
        elif line == "add":
            return Command.ADD
        elif line == "mul":
            return Command.MUL
        elif line == "sub":
            return Command.SUB
        elif line == "div":
            return Command.DIV
        elif line == "rem":
            return Command.REM
        elif line == "neg":
            return Command.NEG
        elif line == "swap":
            return Command.SWAP
        elif line == "quit":
            return Command.QUIT
        elif line == ":true:":
            return Command.BOOL
        elif line == ":false:":
            return Command.BOOL
        elif line == "and":
            return Command.AND
        elif line == "or":
            return Command.OR
        elif line == "not":
            return Command.NOT
        elif line == "equal":
            return Command.EQUAL
        elif line == "lessThan":
            return Command.LESS
        elif line == "bind":
            return Command.BIND
        elif line == "if":
            return Command.IF
        elif line == "let":
            return Command.LET
        elif line == "end":
            return Command.END
        elif line == ":error:":
            return Command.ERROR
        elif line == "funEnd":
            return Command.FUNEND
        elif line == "call":
            return Command.CALL
        elif line == "return":
            return Command.RETURN
        else:
            return Command.ERROR

    def stream(self, instructions):
        """Evaluation of instructions to commands to procedures on the environment stacks."""
        self.create_stack()
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
                cmd = self.translate(line)
                if cmd == Command.PUSH:
                    expr = self.get_push(line[5:], stack)
                    if type(expr) == Item:
                        stack.push(expr)
                    elif type(expr) == Func:
                        stack.push(expr)
                    else:
                        stack.push(expr)
                elif cmd == Command.FUN:
                    if self.is_func(line):
                        fname, arg = self.get_fname_and_arg(line)
                        stack.create_func(fname, arg)
                        fill = True
                        func_name = fname
                    else:
                        stack.push(":error:")
                elif cmd == Command.INOUT:
                    if self.is_in_out(line):
                        fname, arg = self.get_in_out_params(line)
                        stack.create_io(fname, arg)
                        fill = True
                        func_name = fname
                elif cmd == Command.POP:
                    stack.pop()
                elif cmd == Command.BOOL:
                    expr = self.to_bool(line)
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
                    return stack.items
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
                            key = result.name
                            if key in self.vars:
                                self.vars.update({key: result})
                        for block in self.stacks:
                            key = result.name
                            if type(block) == Stack:
                                if key in block.local_var:
                                    block.local_var.update({key: result})
                elif cmd == Command.IF:
                    stack.logical(cmd)
                elif cmd == Command.LET:
                    stack = self.create_let()
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
                elif cmd == Command.CALL:  # function call
                    if len(stack) < 2:
                        stack.push(":error:")
                    else:
                        func = stack.pop()
                        arg = stack.pop()
                        if type(func) == Func and arg != ":error:":
                            look_up = func.fname
                            if look_up in stack.local_func:
                                if type(arg) == Item:
                                    if arg.name in stack.local_var and arg.value != None:
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
                            look_up = func.fname
                            if look_up in stack.local_func:
                                if type(arg) == Item:
                                    if arg.name in stack.local_var and arg.value != None:
                                        linked_arg = func.set_arg_value(arg)
                                        result, do_push = func.call_function(linked_arg)
                                        if do_push is True:
                                            if type(result) == Item:
                                                stack.push(result.value)
                                            else:
                                                stack.push(result)
                                        for block in self.stacks:
                                            if type(result) == Item:
                                                key = result.name
                                                if type(block) == Let:
                                                    block.parent_vars.update({key: result})
                                                    block.local_var.update({key: result})
                                                elif type(block) == Stack:
                                                    if key in block.local_var:
                                                        block.local_var.update({key: result})
                                            else:
                                                if type(block) == Let:
                                                    if key in block.parent_vars:
                                                        v = Item(key, result)
                                                        block.parent_vars.update({key: v})
                                                    if key in block.local_var:
                                                        v = Item(key, result)
                                                        block.local_var.update({key: v})
                                                elif type(block) == Stack:
                                                    if key in block.local_var:
                                                        v = Item(key, result)
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
                        elif type(func) == Item and arg != ":error:":  # function as argument!
                            fun = func.value
                            if type(fun) == Func:
                                look_up = fun.fname
                                if look_up in stack.local_func:
                                    if type(arg) == Item:
                                        if arg.name in stack.local_var and arg.value != None:
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
    """Saves procedures that a function should take on a stack."""
    def __init__(self, fname: str, arg: str, vars_dict: dict, func_dict: dict):
        super().__init__()
        self.fname = fname
        self.arg = arg
        self.parent_vars = vars_dict
        self.parent_funcs = func_dict
        self.instructions = []
        self.return_called = False

    def create_stack(self) -> None:
        """Creates stack and saves it in its local environment."""
        stack = Stack()
        if len(self.vars) > 0:
            for key, value in self.vars.items():
                stack.local_var.update({key: value})
        if len(self.funcs) > 0:
            for key, value in self.parent_funcs.items():
                stack.local_func.update({key: value})
        self.stacks.append(stack)

    def copy(self, line: str) -> None:
        """Saves instructions."""
        self.instructions.append(line)

    def set_arg_value(self, item: Item) -> None:
        """Updates a variables value."""
        if type(item) == Item:
            var = Item(self.arg, item.value)
        else:
            var = Item(self.arg, item)
        self.vars.update({self.arg: var})

    def fill_parent_vars(self) -> None:
        """Copies parent variables."""
        for key, val in self.parent_vars.items():
            self.vars.update({key: val})

    def fill_parent_funcs(self) -> None:
        """Copies parent functions."""
        for key, val in self.parent_funcs.items():
            self.funcs.update({key: val})

    def call_function(self):
        """Executes function instructions."""
        result = self.stream(self.instructions)
        if type(result) == Item:
            return result.value
        else:
            return result


class InOut(Environment):
    """Saves procedures that a InOut function should take on a stack."""
    def __init__(self, fname: str, arg: str, vars_dict: dict, func_dict: dict):
        super().__init__()
        self.fname = fname
        self.arg = arg
        self.parent_vars = vars_dict
        self.parent_funcs = func_dict
        self.instructions = []

    def create_stack(self):
        """Creates stack and saves it in its local environment."""
        s = Stack()
        if len(self.vars) > 0:
            for key, value in self.vars.items():
                s.local_var.update({key: value})
        if len(self.funcs) > 0:
            for key, value in self.parent_funcs.items():
                s.local_func.update({key: value})
        self.stacks.append(s)

    def copy(self, line: str):
        """Saves instructions."""
        self.instructions.append(line)

    def set_arg_value(self, item: Item) -> Item:
        """Updates a variables value."""
        if type(item) == Item:
            var = Item(self.arg, item.value)
            var.alias = item.name
        else:
            var = Item(self.arg, item)
        self.vars.update({self.arg: var})
        return var

    def fill_parent_vars(self) -> None:
        """Copies parent variables."""
        for key, val in self.parent_vars.items():
            self.vars.update({key: val})

    def fill_parent_funcs(self) -> None:
        """Copies parent variables."""
        for key, val in self.parent_funcs.items():
            self.funcs.update({key: val})

    def call_function(self, arg: Item) -> (Item,False):
        """Executes InOut function instructions."""
        return_called = self.stream(self.instructions)
        if return_called is None:
            reference = arg.alias
            for key, val in self.vars.items():
                var = self.vars.get(key)
                if var.alias == reference:
                    if var.value != arg.value:
                        name = var.alias
                        item = Item(name, var.value)
                        return item, False
        else:
            reference = arg.alias
            for key, val in self.vars.items():
                var = self.vars.get(key)
                if var.alias == reference:
                    if var.value != arg.value:
                        name = var.alias
                        item = Item(name, var.value)
                        return item, True
