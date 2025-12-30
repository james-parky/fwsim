from .tokens import Position
from typing import Callable, Optional, Tuple


EOF = str(0)


class Reader:
    _source: str
    _peek: Optional[str]
    _peek_pos: Position
    _next_pos: Position
    _head: int

    def __init__(self, source: str) -> None:
        self._source = source
        self._peek = None
        self._peek_pos = Position.undefined()
        self._next_pos = Position(1, 1)
        self._head = 0

    def next(self) -> Tuple[Optional[str], Position]:
        ret, pos = self.peek()

        self._peek = None
        return (ret, pos)

    def peek(self) -> Tuple[Optional[str], Position]:
        if self._peek is None:
            self._read_next()

        return (self._peek, self._peek_pos)

    def skip_whitespace(self) -> None:
        self.skip_while(lambda c: c.isspace())

    def skip_while(self, pred: Callable[[str], bool]) -> None:
        _, _ = self.take_while(pred)

    def take_while(self, pred: Callable[[str], bool]) -> Tuple[str, Position]:
        ret = ""
        _, pos = self.peek()

        while True:
            peek, _ = self.peek()
            if peek is None or not pred(peek):
                return (ret, pos)

            ret += peek
            self._peek = None

    def must_chomp(self, expect: str) -> Position:
        got, pos = self.next()

        if got != expect:
            raise RuntimeError(f"reader.must_chomp({expect}): got {got}")

        return pos

    def _read_next(self) -> None:
        if self._peek is not None:
            raise RuntimeError("called _read_next() with empty string as peek value")

        if self._head >= len(self._source):
            self._peek = None
            self._peek_pos = self._next_pos
            return

        self._peek = self._source[self._head]
        self._peek_pos = self._next_pos
        self._next_pos = self._next_pos.add(self._peek)
        self._head += 1
