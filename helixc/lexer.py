from dataclasses import dataclass
from typing import Optional

from ply import lex

keywords = {
    'def': 'DEF',
    'var': 'VAR',
    'let': 'LET',
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'for': 'FOR',
    'return': 'RETURN',
    'true': 'TRUE',
    'false': 'FALSE',
}

tokens = (
    *keywords.values(),
    'ID',
    'INTEGER',
    'FLOAT',
    'STRING',
    'ASSIGN',
    'PLUS',
    'MINUS',
    'BANG',
    'TILDE',
    'MUL',
    'DIV',
    'MOD',
    'BITWISE_AND',
    'BITWISE_XOR',
    'BITWISE_OR',
    'LOGICAL_AND',
    'LOGICAL_OR',
    'LPAREN',
    'RPAREN',
    'LT',
    'LE',
    'GT',
    'GE',
    'NE',
    'EQ',
    'COMMA',
    'COLON',
    'SEMI',
    'ARROW',
    'LBRACE',
    'RBRACE',
    'NEWLINE',
    'EOF',
)

t_ASSIGN = r'='
t_PLUS = r'\+'
t_MINUS = r'-'
t_MUL = r'\*'
t_DIV = r'/'
t_MOD = r'%'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LT = r'<'
t_LE = r'<='
t_GT = r'>'
t_GE = r'>='
t_EQ = r'=='
t_NE = r'!='
t_BITWISE_AND = r'&'
t_BITWISE_XOR = r'\^'
t_BITWISE_OR = r'\|'
t_LOGICAL_AND = r'&&'
t_LOGICAL_OR = r'\|\|'
t_BANG = r'!'
t_TILDE = r'~'
t_COMMA = r'\,'
t_COLON = r':'
t_SEMI = r';'
t_ARROW = r'->'
t_LBRACE = r'\{'
t_RBRACE = r'\}'


t_ignore = " \t"


def t_ID(t):
    r"""[_a-zA-Z][_a-zA-Z0-9]*"""
    keyword_type = keywords.get(t.value)
    if keyword_type is not None:
        t.type = keyword_type
    return t


def t_INTEGER(t):
    r"""\d+"""
    t.value = int(t.value)
    return t


def t_FLOAT(t):
    r"""((\d*\.\d+)([Ee][+-]?\d+)?|([1-9]\d*[Ee][+-]?\d+))"""
    t.value = float(t.value)
    return t


def t_STRING(t):
    r"""\".*?\""""
    t.value = t.value[1:-1]
    return t


def t_newline(t):
    r"""\n+"""
    t.type = 'NEWLINE'
    t.lexer_impl.lineno += len(t.value)
    return t


def t_comment(t):
    r"""\s*//[^\n]*"""
    pass


def t_error(t):
    print('Illegal character "%s"' % t.value)
    t.lexer_impl.skip(1)


@dataclass
class Token:
    type: str
    text: Optional[bytes]
    line: int
    column: int
    position: int
    len: int

    @property
    def value(self):
        return self.text


class Lexer:
    def __init__(self):
        self.lexer_impl = lex.lex()
        self.token_stream = iter(())

    def scan(self, source):
        self.lexer_impl.input(source.decode())

        line_number = 0
        line_offset = 0
        position = 0
        for token in self.lexer_impl:
            position = token.lexpos
            if token.type == 'NEWLINE':
                line_number += 1
                line_offset = position + 1
            else:
                yield Token(
                    type=token.type,
                    text=token.value.encode(),
                    line=line_number,
                    column=position - line_offset,
                    position=position,
                    len=len(token.value)
                )

        yield Token('EOF', None, line_number, position - line_offset, position, 0)


def make_lexer():
    return Lexer()
