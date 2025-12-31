from .tokens import Position, Token, TokenType
import pytest


@pytest.mark.parametrize(
    "orig,c,exp",
    [
        (Position(1, 1), "a", Position(1, 2)),
        (Position(1, 10), "\n", Position(2, 1)),
    ],
)
def test_position_add(orig: Position, c: str, exp: Position):
    got = orig.add(c)

    assert got.line == exp.line
    assert got.col == exp.col

def test_position_undefined():
    u = Position.undefined()

    assert(u.line == 0)
    assert(u.col == 0)
