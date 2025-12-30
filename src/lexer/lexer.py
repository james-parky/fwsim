from typing import Optional
from .reader import Reader
from .tokens import Token, TokenType


class Lexer:
    _reader: Reader
    _peek: Optional[Token]

    def __init__(self, input_: str) -> None:
        self._reader = Reader(input_)
        self._peek = None

    def next(self) -> Optional[Token]:
        ret = self.peek()
        self._peek = None

        return ret

    def peek(self) -> Optional[Token]:
        if self._peek is None:
            self._read_next()

        ret = self._peek
        self._peek = None
        return ret

    def _read_next(self):
        if self._peek is not None:
            raise ValueError("Lexer._read_next when peek is not None")

        self._reader.skip_whitespace()

        peeked, peeked_pos = self._reader.peek()

        if peeked is None:
            self._peek = None
            return

        if peeked == "#":
            self._peek = self._read_comment()

        elif peeked in "{}()[],.:;/":
            token_types = {
                "{": TokenType.L_CURLY,
                "}": TokenType.R_CURLY,
                "(": TokenType.L_PAREN,
                ")": TokenType.R_PAREN,
                "[": TokenType.L_SQAURE,
                "]": TokenType.R_SQUARE,
                ",": TokenType.COMMA,
                ".": TokenType.DOT,
                ":": TokenType.COLON,
                ";": TokenType.SEMI_COLON,
                "/": TokenType.FORWARD_SLASH,
            }

            self._reader.must_chomp(peeked)
            self._peek = Token(token_types[peeked], peeked, peeked_pos)

        elif peeked == '"':
            self._peek = self._read_string_literal()

        else:
            if peeked == str(0):
                self._peek = Token.eof()
            else:
                self._peek = self._read_alnum()

    def _read_string_literal(self) -> Token:
        self._reader.must_chomp('"')
        ret, pos = self._reader.take_while(lambda c: c.isascii() and c != '"')
        self._reader.must_chomp('"')

        return Token(TokenType.STRING_LITERAL, ret, pos)

    def _read_comment(self) -> Token:
        self._reader.must_chomp("#")
        ret, pos = self._reader.take_while(lambda c: c != "\n")

        return Token(TokenType.COMMENT, ret, pos)

    def _read_alnum(self) -> Token:
        s, pos = self._reader.take_while(lambda c: c.isalnum())

        if len(s) == 0:
            return Token(TokenType.ILLEGAL, s, pos)
        
        if all(c.isdigit() for c in s):
            return Token(TokenType.INTEGER_LITERAL, s, pos)

        return Token(Token.keyword_or_ident(s), s, pos)


if __name__ == "__main__":
    lexer = Lexer('test;234;:,/{}()[]')
    while True:
        p = lexer.next()
        if p is None:
            break
        print(p)
