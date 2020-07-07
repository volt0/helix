from typing import Iterator

from ply import yacc

from helixc import ast
from helixc.lexer import Token, tokens

tokens = tokens


def p_translation_unit_empty(p):
    """
    translation_unit : EOF
    """
    p[0] = []


def p_translation_unit(p):
    """
    translation_unit : declarations_list EOF
    """
    p[0] = p[1]


def p_declarations_list_1(p):
    """
    declarations_list : declaration
    """
    p[0] = [p[1]]


def p_declarations_list_n(p):
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
    p[0] = ast.FunctionDeclaration(p[2], p[3], p[4], p[5])


def p_arglist_declaration_empty(p):
    """
    arglist_declaration : LPAREN RPAREN
    """
    p[0] = []


def p_arglist_declaration(p):
    """
    arglist_declaration : LPAREN arglist RPAREN
    """
    p[0] = p[2]


def p_arglist_1(p):
    """
    arglist : argument
    """
    p[0] = [p[1]]


def p_arglist_n(p):
    """
    arglist : arglist COMMA argument
    """
    p[0] = p[1]
    p[0].append(p[3])


def p_argument(p):
    """
    argument : ID COLON type_signature
    """
    p[0] = ast.Argument(p[1], p[3])


def p_function_return_type_empty(p):
    """
    function_return_type :
    """
    p[0] = None


def p_function_return_type(p):
    """
    function_return_type : COLON type_signature
    """
    p[0] = p[2]


def p_type_signature(p):
    """
    type_signature : ID
    """
    p[0] = ast.TypeSignature(p[1])


def p_compound_stmt(p):
    """
    compound_stmt : stmt_block
    """
    p[0] = p[1]


def p_stmt_block_empty(p):
    """
    stmt_block : LBRACE RBRACE
    """
    p[0] = []


def p_stmt_block(p):
    """
    stmt_block : LBRACE stmtlist RBRACE
    """
    p[0] = p[2]


def p_stmtlist_1(p):
    """
    stmtlist : stmt
    """
    p[0] = [p[1]]


def p_stmtlist_n(p):
    """
    stmtlist : stmtlist stmt
    """
    p[0] = p[1]
    p[0].append(p[2])


def p_stmt_var(p):
    """
    stmt : variable_signature ASSIGN expr SEMI
    """
    p[0] = ast.VariableInitialization(p[1], p[3])


def p_variable_signature(p):
    """
    variable_signature : variable_mode ID variable_type
    """
    p[0] = ast.VariableSignature(p[2], p[3], mode=p[1])


def p_variable_mode_let(p):
    """
    variable_mode : LET
    """
    p[0] = ast.VariableMode.let


def p_variable_mode_var(p):
    """
    variable_mode : VAR
    """
    p[0] = ast.VariableMode.var


def p_variable_type_empty(p):
    """
    variable_type :
    """
    p[0] = None


def p_variable_type(p):
    """
    variable_type : COLON type_signature
    """
    p[0] = p[2]


def p_stmt_return_void(p):
    """
    stmt : RETURN SEMI
    """
    p[0] = ast.ReturnVoid()


def p_stmt_return_expr(p):
    """
    stmt : RETURN expr SEMI
    """
    p[0] = ast.Return(p[2])


def p_expr_constant(p):
    """
    expr : constant
    """
    p[0] = p[1]


def p_constant_integer_literal(p):
    """
    constant : INTEGER
    """
    p[0] = ast.IntegerLiteral(p[1])


def p_constant_float_literal(p):
    """
    constant : FLOAT
    """
    p[0] = ast.FloatLiteral(p[1])


def p_constant_true(p):
    """
    constant : TRUE
    """
    p[0] = ast.BooleanLiteral(True)


def p_constant_false(p):
    """
    constant : FALSE
    """
    p[0] = ast.BooleanLiteral(False)


def p_error(p):
    raise SyntaxError(p)


class Parser(object):
    def __init__(self):
        self.parser_impl = yacc.yacc(start='translation_unit')
        self.debug = False

    def parse(self, stream: Iterator[Token]):
        lexer_adaptor = LexerAdaptor(stream)
        result = self.parser_impl.parse(lexer=lexer_adaptor, debug=self.debug)
        return result


class LexerAdaptor:
    def __init__(self, stream: Iterator[Token]):
        self.stream = stream

    def token(self):
        try:
            return next(self.stream)
        except StopIteration:
            return None


def make_parser():
    return Parser()
