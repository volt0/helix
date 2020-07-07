import pytest

from helixc.ast import FunctionDeclaration, TypeSignature, Argument
from helixc.lexer import Token

TEST_PARAMS_FUNCTIONS = [
    (
        [
            Token('DEF'),
            Token('ID', text=b'a'),
            Token('LPAREN'),
            Token('RPAREN'),
            Token('LBRACE'),
            Token('RBRACE'),
            Token('EOF'),
        ],
        [
            FunctionDeclaration(
                name='a',
                arguments=[],
                return_type=None,
                body=[]
            )
        ]
    ),
    (
        [
            Token('DEF'),
            Token('ID', b'a'),
            Token('LPAREN'),

            Token('ID', text=b'arg1'),
            Token('COLON'),
            Token('ID', text=b'Int'),
            Token('COMMA'),

            Token('ID', text=b'arg2'),
            Token('COLON'),
            Token('ID', text=b'Int'),

            Token('RPAREN'),
            Token('COLON'),
            Token('ID', text=b'Int'),
            Token('LBRACE'),
            Token('RBRACE'),
            Token('EOF'),
        ],
        [
            FunctionDeclaration(
                name='a',
                arguments=[
                    Argument('arg1', type=TypeSignature(name='Int')),
                    Argument('arg2', type=TypeSignature(name='Int')),
                ],
                return_type=TypeSignature(name='Int'),
                body=[]
            )
        ]
    ),
]


@pytest.mark.parametrize('stream,ref_ast', TEST_PARAMS_FUNCTIONS)
def test_parser(stream, ref_ast, parser):
    assert parser.parse(iter(stream)) == ref_ast


@pytest.fixture
def parser():
    from helixc.parser import make_parser
    return make_parser()
