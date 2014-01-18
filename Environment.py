class Environment(object):
    def __init__(self, vars=(), args=(), higher_environment=None):
        self.dict = dict(zip(vars, args))
        self.higher_environment = higher_environment

    def update(self, other_dict):
        self.dict.update(other_dict)

    def get(self, key):
        if key in self.dict:
            return self.dict[key]
        elif self.higher_environment:
            return self.higher_environment.get(key)
        else:
            raise UnboundLocalError("Variable %s is not defined." % key)

    def set(self, key, value):
        if key in self.dict:
            self.dict[key] = value
        elif self.higher_environment:
            self.higher_environment.set(key, value)
        else:
            raise Exception("Variable %s was not already defined." % key)

    def define(self, key, value):
        if not self.contains(key):
            self.dict[key] = value
        else:
            raise Exception("%s: this name was defined previously and cannot be re-defined" % key)

    def contains(self, key):
        if key in self.dict:
            return True
        elif self.higher_environment:
            return self.higher_environment.contains(key)
        else:
            return False

    def get_correct_environment(self, key):
        return self if (key in self) else self.higher_environment.get(key)


def make_default_environment():
    import math, operator

    empty_environment = Environment()
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