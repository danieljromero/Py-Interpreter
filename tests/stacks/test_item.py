from interpreter.stacks import Item

class TestItem:
    def test__init__(self):
        pass

    def test_add(self):
        x = Item('x',1)
        y = Item('y',2)
        assert x + y == 3
        assert x + 2 == 3
        assert 1 + y == 3

    def test_sub(self):
        x = Item('x',1)
        y = Item('y',2)
        assert x - y == -1
        assert x - 2 == -1
        assert 1 - y == -1

    def test_mul(self):
        x = Item('x',2)
        y = Item('y',3)
        assert x * y == 6
        assert x * 2 == 4
        assert 1 * y == 3

    def test_div(self):
        x = Item('x',2)
        y = Item('y',2)
        assert x // y == 1
        assert x // 2 == 1
        assert 1 // y == 0

    def test_mod(self):
        x = Item('x',4)
        y = Item('y',4)
        assert x % y == 0
        assert x % 2 == 0
        assert 1 % y == 1

    def test_neg(self):
        x = Item('x',4)
        assert -x == -4

    def test_bool(self):
        x = Item('x',True)
        assert bool(x) == True

    def test_and(self):
        # can't override 'and' operator
        x = Item('x',True)
        y = Item('y',True)
        z = Item('z',False)
        w = Item('w',False)
        assert x & y == True
        assert y & z == False
        assert z & x == False
        assert z & w == False
        assert x & True == True
        assert x & False == False
        assert False & x == False
        assert z & False == False

    def test_or(self):
        # can't override 'or' operator
        x = Item('x',True)
        y = Item('y',True)
        z = Item('z',False)
        w = Item('w',False)
        assert x | y == True
        assert y | z == True
        assert z | x == True
        assert z | w == False
        assert x | True == True
        assert x | False == True
        assert False | x == True
        assert z | False == False

    def test_eq(self):
        x = Item('x',True)
        y = Item('y',True)
        z = Item('z',False)
        w = Item('w',False)
        assert (x == y) == True
        assert (y == z) == False
        assert (x == True) == True
        assert (x == False) == False

    def test_lt(self):
        x = Item('x',1)
        y = Item('y',2)
        assert (x < y) == True
        assert (y < x) == False
        assert (x < 2) == True
        assert (y < 1) == False
