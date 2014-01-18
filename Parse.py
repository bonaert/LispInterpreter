Symbol = str


def parse(x):
    """ Tokenize and parse a Lisp expression"""
    tokens = tokenize(x)
    return parse_tokens(tokens)


def tokenize(x):
    """ Convert a string into a list of tokens """
    return x.replace('(', ' ( ').replace(')', ' ) ').split()


def parse_tokens(tokens):
    """ Parses the tokens and converts them into a Python representation. """
    if len(tokens) == 0:
        raise Exception('Reached end of file unexpectedly.')
    token = tokens.pop(0)

    if token == '(':
        return parse_expression(tokens)
    elif token == ')':
        raise Exception('Unexpected )')
    else:
        return atom(token)


def parse_expression(tokens):
    parsed_expr = []
    while tokens[0] != ')':
        parsed_expr.append(parse_tokens(tokens))

    tokens.pop(0) # remove the remaining ')'

    return parsed_expr


def atom(token):
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            return Symbol(token)
