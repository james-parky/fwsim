from fwsim.parser.parser import Parser
from fwsim.lexer.lexer import Lexer

def main(argv: list[str] | None = None) -> int:
    code = """table inet filter {
        chain input {
            type filter hook input priority 0;

            ip saddr 192.168.1.0/24 accept
            drop
        }    
    }
    """
    p = Parser(Lexer(code))
    ast = p.parse()
    print(ast)

    return 0
