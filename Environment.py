class Environment(dict):
    def __init__(self, vars=(), args=(), higher_environment=None):
        self.update(zip(vars, args))
        self.higher_environment = higher_environment

    def get_correct_environment(self, key):
        return self if (key in self) else self.higher_environment.get(key)

def make_default_environment(empty_environment):
    import math, operator
    empty_environment.update(vars(math))
    empty_environment.update({
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.truediv,
        'not': operator.not_,
        '=': operator.eq,
        '>': operator.gt,
        '>=': operator.ge,
        '<': operator.lt,
        '<=': operator.le,
        'equal?': operator.eq,
        'eq?': operator.eq,
        'len': len,
        'cons': lambda x, y: [x] + y,
        'car': lambda x: x[0],
        'cdr': lambda x: x[1:],
        'append': operator.add,
        'list': lambda *x: list(x),
        'list?': lambda x: isinstance(x, list),
        'null?': lambda x: x == [],
        'symbol?': lambda x: isinstance(x, str)
    })
    return empty_environment