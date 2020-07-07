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
def test_functions(stream, ref_ast, parser):
    assert parser.parse(iter(stream)) == ref_ast


TEST_PARAMS_STMT = [
    pytest.param(
        [
            # def f() {}
            Token('LET'),
            Token('ID', 'a'),
            Token('ASSIGN'),
            Token('INTEGER', 1),
            Token('SEMI'),

            Token('VAR'),
            Token('ID', 'b'),
            Token('ASSIGN'),
            Token('INTEGER', 2),
            Token('SEMI'),
        ],
        [
            ast.VariableInitialization(
                variable=ast.VariableSignature('a', type=None, mode=ast.VariableMode.let),
                value=ast.IntegerLiteral(1)
            ),
            ast.VariableInitialization(
                variable=ast.VariableSignature('b', type=None, mode=ast.VariableMode.var),
                value=ast.IntegerLiteral(2)
            ),
        ],
        id='let_and_var'
    ),

    pytest.param(
        [
            # def f() {}
            Token('LET'),
            Token('ID', 'a'),
            Token('COLON'),
            Token('ID', 'Int'),
            Token('ASSIGN'),
            Token('INTEGER', 0),
            Token('SEMI'),
        ],
        [
            ast.VariableInitialization(
                variable=ast.VariableSignature('a', type=ast.TypeSignature(name='Int'), mode=ast.VariableMode.let),
                value=ast.IntegerLiteral(0)
            ),
        ],
        id='let_typed'
    ),
]


@pytest.mark.parametrize('stream_part,ref_ast', TEST_PARAMS_STMT)
def test_stmt(stream_part, ref_ast, parser):
    stream = iter([
        Token('DEF'),
        Token('ID', 'f'),
        Token('LPAREN'),
        Token('RPAREN'),
        Token('COLON'),
        Token('ID', 'Int'),
        Token('LBRACE'),
        *stream_part,
        Token('RBRACE'),
        Token('EOF'),
    ])
    parse_result = parser.parse(stream)
    assert parse_result[0].body == ref_ast


@pytest.fixture
def parser():
    from helixc.parser import make_parser
    return make_parser()
