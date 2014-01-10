from Environment import Environment, make_default_environment

default_env = make_default_environment(Environment())


def eval(x, environment=default_env):
    if isinstance(x, str):
        return environment.get_correct_environment(x)[x]
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
        environment.get_correct_environment(var)[var] = eval(expr, environment)
    elif x[0] == 'define':
        (_, var, expr) = x
        environment[var] = eval(expr, environment)
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