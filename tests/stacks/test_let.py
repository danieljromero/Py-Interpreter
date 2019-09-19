from interpreter.stacks import Let, Item

class TestLet:
    def test_init(self):
        let = Let({},{})

    def test_push_var(self):
        let = Let({},{})
        let.push(Item('a',1))
        let.push(Item('b',1))
        assert len(let) == 2

    def test_bind(self):
        parent_var = {'a':Item('a', 0)}
        let = Let(parent_var,{})
        let.push(Item('a',None))  # pushes var from parent instead
        let.push(2)
        assert len(let) == 2
        item = let.bind()
        assert isinstance(item, Item) == True
        assert item.value == 2
        assert parent_var.get('a').value == 2
        assert len(let) == 1

    def test_create_func(self):
        let = Let({},{})
        let.create_func('function1','x')

    def test_create_io(self):
        let = Let({},{})
        let.create_io('InOut1','x')
