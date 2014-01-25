import Symbol


def read(x):
    """ Read, tokenize and parse a Lisp expression"""
    input_port = Symbol.InputPort(x)
    return parse_tokens(input_port)


def parse(input_port):
    """ Tokenize and parse a Lisp expression"""
    return parse_tokens(input_port)


def tokenize(x):
    """ Convert a string into a list of tokens """
    return x.replace('(', ' ( ').replace(')', ' ) ').split()


def parse_tokens(input_port):
    """ Parses the tokens from an input port and converts them into a Python representation. """
    first_token = input_port.read_token()

    if first_token == Symbol.eof_object:
        return Symbol.eof_object
    return parse_token(first_token, input_port)


def parse_token(token, input_port):
    """ Parses the tokens and converts them into a Python representation. """
    if token == '(':
        return parse_expression(token, input_port)
    elif token == ')':
        raise Exception('Unexpected )')
    elif token == Symbol.eof_object:
        raise Exception('Unexpected EOF in list.')
    else:
        return atom(token)


def parse_expression(token, input_port):
    """ Parse a Lisp expression into its corresponding Python representation"""
    parsed_expr = []
    while True:
        token = input_port.read_token()

        if token == ')':
            return parsed_expr
        else:
            parsed_expr.append(parse_token(token, input_port))


def atom(token):
    if token == '#t':
        return True
    elif token == '#f':
        return False
    elif token[0] == '"':
        return token[1:-1]

    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            try:
                return complex(token.replace('i', 'j', 1))
            except ValueError:
                return Symbol.make_symbol(token)
