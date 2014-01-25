import re


class Symbol(str): pass


def make_symbol(s, symbol_table={}):
    if s not in symbol_table:
        symbol_table[s] = Symbol(s)

    return symbol_table[s]


eof_object = Symbol('#<eof-object>')


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
        except:
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