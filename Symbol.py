class Symbol(str): pass


def make_symbol(s, symbol_table={}):
    if s not in symbol_table:
        symbol_table[s] = Symbol(s)

    return symbol_table[s]


eof_object = Symbol('#<eof-object>')
_quote, _if, _set, _define, _lambda, _begin, _definemacro, = map(make_symbol,
                                                                 "quote   if   set!  define   lambda   begin   define-macro".split())

_quasiquote, _unquote, _unquotesplicing = map(make_symbol, "quasiquote   unquote   unquote-splicing".split())


