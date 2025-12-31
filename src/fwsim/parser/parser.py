from typing import Optional
from fwsim.lexer.lexer import Lexer
from fwsim.ast.ast import Family, Ruleset, TableBlock
from fwsim.lexer.tokens import TokenType


class Parser:
    lexer: Lexer

    def __init__(self, lexer: Lexer) -> None:
        self.lexer = lexer

    def parse(self) -> Optional[Ruleset]:
        ruleset = Ruleset()

        while True:
            peek = self.lexer.peek()

            if peek is None:
                return ruleset

            table_block = self._parse_table_block()
            ruleset.table_blocks.append(table_block)


    def _parse_table_block(self) -> TableBlock:
        # TABLE family IDENTIFIER L_CURLY chain* R_CURLY

        _ = self.lexer.chomp(TokenType.IDENTIFIER, 'table')
        family = self._parse_family()
        ident = self._parse_ident()
        _ = self.lexer.chomp(TokenType.L_CURLY)
        _ = self.lexer.chomp(TokenType.R_CURLY)

        return TableBlock(family, ident, [])

    
    def _parse_ident(self) -> str:
        got = self.lexer.chomp(TokenType.IDENTIFIER)

        return got.value

    def _parse_family(self) -> Family:
        peek = self.lexer.next()
        if peek is None:
            raise RuntimeError("expected family, got None")

        if peek.value == "ip":
            return Family.IP
        elif peek.value == "inet":
            return Family.INET
        elif peek.value == "ip6":
            return Family.IP6

        raise RuntimeError(f"expected family, got {peek}")


