"""Module containing the Token class and associated types used in the lexer."""

from enum import Enum, auto


class Position:
    """A position in some lexable input."""

    line: int
    col: int

    def __init__(self, line: int, col: int) -> None:
        self.line = line
        self.col = col

    def __repr__(self) -> str:
        return f"({self.line}:{self.col})"

    # `c` provided as a string due to limitations of Python's type system.
    def add(self, c: str) -> 'Position':
        """
        Generate the next position given the current one, and the provided
        character. Increment the column count for any character, other than a
        newline; in which case increment the line count.

        Args:
            c (str): The character being read.

        Returns:
            Position: The position of the "cursor" after reading character `c`.
        """

        if c == "\n":
            return Position(self.line + 1, 1)

        return Position(self.line, self.col + 1)

    @staticmethod
    def undefined() -> 'Position':
        """Static method to return a sentinal 'undefined' position in input."""

        return Position(0, 0)


# Introduce interface in the future to lex different token types for different
# languages.
class TokenType(Enum):
    """Types that a lexed token can take."""

    # TODO: needed?
    # Non-textual types types
    UNDEFINED = auto()
    ILLEGAL = auto()
    EOF = auto()
    COMMENT = auto()

    # Primitives
    IDENTIFIER = auto()
    INTEGER_LITERAL = auto()
    STRING_LITERAL = auto()

    # Operators
    L_CURLY = auto()
    R_CURLY = auto()
    L_PAREN = auto()
    R_PAREN = auto()
    L_SQAURE = auto()
    R_SQUARE = auto()
    SEMI_COLON = auto()
    COLON = auto()
    DASH = auto()
    DOT = auto()
    COMMA = auto()
    FORWARD_SLASH = auto()

    # NFT Keywords
    TABLE = auto()
    CHAIN = auto()
    RULE = auto()
    TYPE = auto()
    HOOK = auto()
    PRIORITY = auto()
    POLICY = auto()
    ACCEPT = auto()
    DROP = auto()
    IP = auto()
    INET = auto()
    IP6 = auto()
    FILTER = auto()
    INPUT = auto()
    OUTPUT = auto()
    FORWARD = auto()
    PREROUTING = auto()
    POSTROUTING = auto()
    SADDR = auto()
    DADDR = auto()
    SPORT = auto()
    DPORT = auto()
    TCP = auto()
    UDP = auto()


class Token:
    """A lexed unit from some input."""

    type_: TokenType
    # TODO: bytes?
    value: str
    position: Position

    def __init__(self, type_: TokenType, value: str, pos: Position) -> None:
        self.type_ = type_
        self.value = value
        self.position = pos

    def __repr__(self) -> str:
        return f"{self.type_}: [{self.value}]: {self.position}"

    def is_type(self, t: TokenType) -> bool:
        """
        Check if this token is of type `t`.

        Args:
            t: (TokenType): The type to check equality against.

        Returns:
            bool: Whether or not it matches
        """

        return self.type_ == t

    @staticmethod
    def eof() -> 'Token':
        """
        A sentinal value for a token representing the end of lexible input.
        """

        return Token(TokenType.EOF, "", Position.undefined())

    @staticmethod
    def keyword_or_ident(ident: str) -> TokenType:
        """
        If `ident` is a recognised keyword, return the corresponding specific
        `TokenType`, else return `TokenType.IDENTIFIER`.

        Args:
            ident (str): The read identifier.

        Returns:
            TokenType: The correct keyword `TokenType`, or
                       `TokenType.IDENTIFIER`.
        """

        keywords = {
            "table": TokenType.TABLE,
            "chain": TokenType.CHAIN,
            "rule": TokenType.RULE,
            "type": TokenType.TYPE,
            "hook": TokenType.HOOK,
            "priority": TokenType.PRIORITY,
            "policy": TokenType.POLICY,
            "accept": TokenType.ACCEPT,
            "drop": TokenType.DROP,
            "ip": TokenType.IP,
            "inet": TokenType.INET,
            "ip6": TokenType.IP6,
            "filter": TokenType.FILTER,
            "input": TokenType.INPUT,
            "output": TokenType.OUTPUT,
            "forward": TokenType.FORWARD,
            "prerouting": TokenType.PREROUTING,
            "postrouting": TokenType.POSTROUTING,
            "saddr": TokenType.SADDR,
            "daddr": TokenType.DADDR,
            "sport": TokenType.SPORT,
            "dport": TokenType.DPORT,
            "tcp": TokenType.TCP,
            "udp": TokenType.UDP,
        }

        if ident in keywords:
            return keywords[ident]

        return TokenType.IDENTIFIER


UNDEFINED = Token(TokenType.UNDEFINED, "", Position(0, 0))
