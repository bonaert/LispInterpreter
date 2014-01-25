import re
import Symbol
from Symbol import eof_object, quotes


def read(x):
    """ Read, tokenize and parse a Lisp expression"""
    input_port = InputPort(x)
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
    elif token in quotes:
        return [quotes[token], parse_tokens(input_port)]
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


class InputPort(object):
    """An input port. Retains a line of chars."""
    tokenizer = r'''\s*(,@|[('`,)]|"(?:[\\].|[^\\"])*"|;.*|[^\s('"`,;)]*)(.*)'''
    matcher = re.compile(tokenizer)

    def __init__(self, stream):
        self.stream = stream
        self.line = ''

    def read_line(self):
        try:
            return self.stream.readline()
        except Exception as e:
            return self.stream

    def read_token(self):
        """Return the next token, reading new text into line buffer if needed."""
        while True:
            if self.line == '':
                self.line = self.read_line()

            if self.line == '':
                return eof_object

            token, self.line = self.matcher.match(self.line).groups()
            if token != '' and not token.startswith(';'):
                return token