from .parser.parser import Parser
from .lexer.lexer import Lexer

def main(argv: list[str] | None = None) -> int:
    code = "table inet filter {}"
    p = Parser(Lexer(code))
    
    ast = p.parse()
    print(ast)

    return 0
