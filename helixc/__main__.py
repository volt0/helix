from helixc.lexer import make_lexer, filter_newlines, filter_add_eof
from helixc.parser import make_parser


def main():
    sample_code = b'''
def a(): Int {}
'''
    lexer = make_lexer()
    stream = lexer.scan(sample_code)
    stream = filter_add_eof(stream)
    stream = filter_newlines(stream)

    parser = make_parser()
    print(parser.parse(stream))


if __name__ == '__main__':
    main()
