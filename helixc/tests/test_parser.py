import pytest

from helixc import ast
from helixc.lexer import Token

TEST_PARAMS_FUNCTIONS = [
    pytest.param(
        [
            # def f() {}
            Token('DEF'),
            Token('ID', 'f'),
            Token('LPAREN'),
            Token('RPAREN'),
            Token('LBRACE'),
            Token('RBRACE'),
            Token('EOF'),
        ],
        [
            ast.FunctionDeclaration(
                name='f',
                arguments=[],
                return_type=None,
                body=[]
            )
        ],
        id='minimal_func'
    ),

    pytest.param(
        [
            # def f
            Token('DEF'),
            Token('ID', 'f'),
            # (arg1: Int, arg2: Int)
            Token('LPAREN'),
            Token('ID', 'arg1'),
            Token('COLON'),
            Token('ID', 'Int'),
            Token('COMMA'),
            Token('ID', 'arg2'),
            Token('COLON'),
            Token('ID', 'Int'),
            Token('RPAREN'),
            # : Int
            Token('COLON'),
            Token('ID', 'Int'),
            # {}
            Token('LBRACE'),
            Token('RBRACE'),
            Token('EOF'),
        ],
        [
            ast.FunctionDeclaration(
                name='f',
                arguments=[
                    ast.Argument('arg1', type=ast.TypeSignature(name='Int')),
                    ast.Argument('arg2', type=ast.TypeSignature(name='Int')),
                ],
                return_type=ast.TypeSignature(name='Int'),
                body=[]
            )
        ],
        id='args'
    ),

    pytest.param(
        [
            # def f()
            Token('DEF'),
            Token('ID', 'f'),
            Token('LPAREN'),
            Token('RPAREN'),
            Token('LBRACE'),
            # return;
            Token('RETURN'),
            Token('SEMI'),
            Token('RBRACE'),
            Token('EOF'),
        ],
        [
            ast.FunctionDeclaration(
                name='f',
                arguments=[],
                return_type=None,
                body=[
                    ast.ReturnVoid()
                ]
            )
        ],
        id='return_void'
    ),

    pytest.param(
        [
            # def f(): Int
            Token('DEF'),
            Token('ID', 'f'),
            Token('LPAREN'),
            Token('RPAREN'),
            Token('COLON'),
            Token('ID', 'Int'),
            Token('LBRACE'),
            # return 99;
            Token('RETURN'),
            Token('INTEGER', 99),
            Token('SEMI'),
            Token('RBRACE'),
            Token('EOF'),
        ],
        [
            ast.FunctionDeclaration(
                name='f',
                arguments=[],
                return_type=ast.TypeSignature(name='Int'),
                body=[
                    ast.Return(ast.IntegerLiteral(99))
                ]
            )
        ],
        id='return_value'
    ),
]


@pytest.mark.parametrize('stream,ref_ast', TEST_PARAMS_FUNCTIONS)
def test_parser(stream, ref_ast, parser):
    assert parser.parse(iter(stream)) == ref_ast


@pytest.fixture
def parser():
    from helixc.parser import make_parser
    return make_parser()
