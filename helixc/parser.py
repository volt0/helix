from typing import Iterator

from ply import yacc

from helixc.ast import Module, FunctionDeclaration, Argument, TypeSignature
from helixc.lexer import Token, tokens

tokens = tokens


def p_module(p):
    """
    module : declarations_list EOF
    """
    p[0] = Module(p[1])


def p_declarations_list_1(p):
    """
    declarations_list : declaration
    """
    p[0] = [p[1]]


def p_declarations_list_2(p):
    """
    declarations_list : declarations_list declaration
    """
    p[0] = p[1]
    p[0].append(p[2])


def p_declaration(p):
    """
    declaration : function_declaration
    """
    p[0] = p[1]


def p_function_declaration(p):
    """
    function_declaration : DEF ID arglist_declaration function_return_type compound_stmt
    """
    p[0] = FunctionDeclaration(p[2].decode(), p[3], p[4], p[5])


def p_arglist_declaration_1(p):
    """
    arglist_declaration : LPAREN RPAREN
    """
    p[0] = []


def p_arglist_declaration_2(p):
    """
    arglist_declaration : LPAREN arglist RPAREN
    """
    p[0] = p[2]


def p_arglist_1(p):
    """
    arglist : argument
    """
    p[0] = [p[1]]


def p_arglist_2(p):
    """
    arglist : arglist COMMA argument
    """
    p[0] = p[1]
    p[0].append(p[3])


def p_argument(p):
    """
    argument : ID
    """
    p[0] = Argument(p[1].decode(), None)


def p_function_return_type(p):
    """
    function_return_type : ARROW ID
    """
    p[0] = TypeSignature(p[2].decode())


def p_compound_stmt(p):
    """
    compound_stmt : LBRACE RBRACE
    """
    p[0] = {}


# def p_error(p):
#     raise SyntaxError(p)


class Parser(object):
    def __init__(self):
        self.parser_impl = yacc.yacc(start='module')

    def parse(self, stream: Iterator[Token]):
        lexer_adaptor = LexerAdaptor(stream)
        result = self.parser_impl.parse(lexer=lexer_adaptor, debug=False)
        return result


class LexerAdaptor:
    def __init__(self, stream: Iterator[Token]):
        self.stream = stream

    def token(self):
        try:
            token = next(self.stream)
            # if self.debug:
            #     print(token)
            return token

        except StopIteration:
            return None


def make_parser():
    return Parser()
