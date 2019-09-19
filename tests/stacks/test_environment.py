from interpreter.stacks import Environment
from interpreter.commands import Command


class TestEnvironment:
    def test_init(self):
        env = Environment()

    def test_create_stack(self):
        env = Environment()
        env.create_stack()

    def test_create_let(self):
        env = Environment()
        env.create_let()

    def test_create_func(self):
        env = Environment()
        env.create_func('function1','x')

    def test_create_in_out(self):
        env = Environment()
        env.create_io('InOut1','x')

    def test_is_fun(self):
        env = Environment()
        fn_single_arg = 'fun stuff b'
        fn_multi_args = 'fun stuff a b'
        assert env.is_func(fn_single_arg) == True
        assert env.is_func(fn_multi_args) == True

    def test_is_not_func(self):
        env = Environment()
        diff_format = 'def fun(a, b):'
        empty = 'fun '
        no_fn_name = 'fun  '
        no_fn_args = 'fun wow'
        repeated_fn_name = 'fun wow wow'
        repeated_fn_args = 'fun wow a a a a a'
        keywords = 'fun fun fun'
        assert env.is_func('') == False
        assert env.is_func(empty) == False
        assert env.is_func(diff_format) == False
        assert env.is_func(no_fn_name) == False
        assert env.is_func(no_fn_args) == False
        assert env.is_func(repeated_fn_name) == False
        assert env.is_func(repeated_fn_args) == False
        assert env.is_func(keywords) == False

    def test_is_push(self):
        env = Environment()
        integer = 'push 1'
        variable = 'push a'
        function = 'push f1'
        assert env.is_push(integer) == True
        assert env.is_push(variable) == True
        assert env.is_push(function) == True

    def test_is_not_push(self):
        env = Environment()
        empty = 'push '
        no_item = 'push  '
        multi_items = 'push 1 2'
        assert env.is_push(empty) == False
        assert env.is_push(no_item) == False
        assert env.is_push(multi_items) == True  # multiple for to functions

    def test_is_int(self):
        env = Environment()
        zero = '0'
        positive = '1'
        negative = '-1'
        assert env.is_int(zero) == True
        assert env.is_int(positive) == True
        assert env.is_int(negative) == True

    def test_is_not_int(self):
        env = Environment()
        alpha = 'a'
        alphanum = 'a1'
        random = '!@#$'
        assert env.is_int(alpha) == False
        assert env.is_int(alphanum) == False
        assert env.is_int(random) == False

    def test_is_in_out(self):
        env = Environment()
        template = 'inOutFun funName arg'
        assert env.is_in_out(template) == True

    def test_is_not_in_out(self):
        env = Environment()
        empty = 'inOutFun  '
        no_fn_name = 'inOutFun '
        no_arg = 'inOutFun funName'
        assert env.is_in_out('') == False
        assert env.is_in_out(empty) == False
        assert env.is_in_out(no_fn_name) == False
        assert env.is_in_out(no_arg) == False

    def test_translate(self):
        env = Environment()
        inst_pop = 'pop'
        inst_fun = 'fun funName arg'
        inst_inout = 'inOutFun funName arg'
        inst_add = 'add'
        inst_mul = 'mul'
        inst_sub = 'sub'
        inst_div = 'div'
        inst_rem = 'rem'
        inst_neg = 'neg'
        inst_swap = 'swap'
        inst_quit = 'quit'
        inst_true = ':true:'
        inst_false = ':false:'
        inst_and = 'and'
        inst_or = 'or'
        inst_not = 'not'
        inst_eq = 'equal'
        inst_lth = 'lessThan'
        inst_bind = 'bind'
        inst_if = 'if'
        inst_let = 'let'
        inst_end = 'end'
        inst_err = ':error:'
        inst_fun_end = 'funEnd'
        inst_call = 'call'
        inst_return = 'return'
        inst_error = 'asddef2er2f2f'
        assert env.translate(inst_pop) == Command.POP
        assert env.translate(inst_fun) == Command.FUN
        assert env.translate(inst_inout) == Command.INOUT
        assert env.translate(inst_add) == Command.ADD
        assert env.translate(inst_mul) == Command.MUL
        assert env.translate(inst_sub) == Command.SUB
        assert env.translate(inst_div) == Command.DIV
        assert env.translate(inst_rem) == Command.REM
        assert env.translate(inst_neg) == Command.NEG
        assert env.translate(inst_swap) == Command.SWAP
        assert env.translate(inst_quit) == Command.QUIT
        assert env.translate(inst_true) == Command.BOOL
        assert env.translate(inst_false) == Command.BOOL
        assert env.translate(inst_and) == Command.AND
        assert env.translate(inst_or) == Command.OR
        assert env.translate(inst_not) == Command.NOT
        assert env.translate(inst_eq) == Command.EQUAL
        assert env.translate(inst_lth) == Command.LESS
        assert env.translate(inst_bind) == Command.BIND
        assert env.translate(inst_if) == Command.IF
        assert env.translate(inst_let) == Command.LET
        assert env.translate(inst_end) == Command.END
        assert env.translate(inst_err) == Command.ERROR
        assert env.translate(inst_fun_end) == Command.FUNEND
        assert env.translate(inst_call) == Command.CALL
        assert env.translate(inst_return) == Command.RETURN
        assert env.translate(inst_error) == Command.ERROR

    def test_stream(self):
        pass
