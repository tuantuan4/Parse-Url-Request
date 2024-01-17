import sys

from sly import Lexer, Parser


class QueryLexer(Lexer):
    tokens = {NAME, EQ, GT, AND, OR, LPAREN, RPAREN, INT}
    ignore = ' \t'

    # Các biểu thức chính quy cho các token
    NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
    EQ = r'eq'
    GT = r'gt'
    AND = r'and'
    OR = r'or'
    # NOT = r'not'
    LPAREN = r'\('
    RPAREN = r'\)'
    INT = r'\d+'
    ignore_newline = r'`'

    # ký tự không xác định
    def error(self, t):
        print(f"Illegal character '{t.value[0]}' at index {t.index}")
        self.index += 1


# Định nghĩa Parser
class QueryParser(Parser):
    tokens = QueryLexer.tokens

    precedence = (
        ('left', OR),
        ('left', AND),
        ('left', EQ, GT),
        ('nonassoc', 'LPAREN', 'RPAREN'),
    )

    def __init__(self):
        self.names = {}

    @_('expr OR expr',
       'expr AND expr')
    def expr(self, p):
        return (p[1], p.expr[0], p[3])

    @_('LPAREN expr RPAREN')
    def expr(self, p):
        return p[2]

    @_('NAME EQ NAME',
       'NAME GT INT')
    def expr(self, p):
        return (p[2], p[1], p[3])

    # def error(self, p):
    #     print("Syntax error")


def parse_query(query):
    lexer = QueryLexer()
    parser = QueryParser()

    tokens = lexer.tokenize(query)
    for token in tokens:
        print(f"Token: {token.type}, Value: {token.value}")
    try:
        result = parser.parse(tokens)
        print(result)
    except Exception:
        print("Unexpected error:", sys.exc_info()[0])


parse_query("name eq makai")
