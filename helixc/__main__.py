from helixc.lexer import make_lexer
from helixc.parser import make_parser


def main():
    sample_code = b'''\
def a() -> Int {}
'''
    lexer = make_lexer()
    stream = lexer.scan(sample_code)

    parser = make_parser()
    print(parser.parse(stream))


if __name__ == '__main__':
    main()
