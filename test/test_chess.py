from chess import Board

from nmr import nmr, types
from nmr.types import chess

import pytest


INDICES = 0, 1, 2, 17, 225289, 82394423423, 80983412412323423
STRATEGIES = (lambda a: a[0]), (lambda a: a[int(len(a) / 2)]), (lambda a: a[-1])
COUNT = 10


@pytest.mark.parametrize("index", INDICES)
def test_rows(index):
    r = chess.index_to_row(index)
    actual = chess.row_to_index(r)
    assert actual == index


def test_roundtrip():
    b = Board()
    name = nmr.str_to_name(b.fen())
    b2 = nmr.name_to_str(name)
    assert b2 == b.gen()


@pytest.mark.parametrize("strategy", STRATEGIES)
def NOT_test_roundtrip(strategies):
    b = Board()
    for i in range(count):
        pass
