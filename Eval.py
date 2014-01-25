from Environment import Environment, make_default_environment


def eval(x, environment=None):
    if environment is None:
        environment = make_default_environment()

    if isinstance(x, Symbol):
        return environment.get(x)
    elif not isinstance(x, list):
        return x
    elif x[0] == 'quote':
        (_, exp) = x
        return exp
    elif x[0] == 'if':
        (_, test, if_body, else_body) = x
        return eval(if_body if eval(test, environment) else else_body, environment)
    elif x[0] == 'set!':
        (_, var, expr) = x
        environment.set(var, eval(expr, environment))
    elif x[0] == 'define':
        (_, var, expr) = x
        environment.define(var, eval(expr, environment))
    elif x[0] == 'lambda':
        (_, vars, body) = x
        return lambda *args: eval(body, Environment(vars, args, environment))
    elif x[0] == 'begin':
        for expr in x[1:]:
            val = eval(expr, environment)
        return val
    else:
        function = eval(x[0], environment)
        args = [eval(expr, environment) for expr in x[1:]]
        return function(*args)


Symbol = str