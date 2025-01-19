import chess

from ..categories import Game
from ..nameable_type import NameableType
from ..radixes import Radixes


class Chess(NameableType[chess.Board]):
    category = Game.CHESS

    @staticmethod
    def index_to_type(i: int) -> chess.Board:
        return chess.Board()

    @staticmethod
    def type_to_str(board: chess.Board) -> str:
        return board.fen()

    @staticmethod
    def type_to_index(b: chess.Board) -> int:
        board, side, castle, ep, half_move, move = b.fen().split()
        ret = RADIXES.encode(
            int(move),
            int(half_move),
            en_passant_to_index(ep),
            *(c in castle for c in CASTLES),
            SIDES.index(side),
            *(row_to_index(b) for b in board.split("/")),
        )
        print('INDEX return', ret)
        return ret

    @staticmethod
    def index_to_type(n: int) -> chess.Board:
        parts = RADIXES.decode(n)
        parts, board = parts[:-8], parts[-8:]
        move, half_move, ep, *castle, side = parts
        assert len(castle) == 4
        parts = (
            "/".join(index_to_row(r) for r in board),
            SIDES[side],
            "".join(c for b, c in zip(castle, CASTLES) if b) or "-",
            index_to_en_passant(ep),
            str(move),
            str(half_move),
        )
        return chess.Board(" ".join(parts))


ALPHABET = "12345678BKNPQRbknpqr"
SIDES = "wb"
CASTLES = "KQkq"
EP_LENGTH = 65

RADIXES = Radixes(
    2, EP_LENGTH, *(2 for c in CASTLES), len(SIDES), *(8 * [len(ALPHABET)])
)


def en_passant_to_index(ep: str) -> int:
    if ep == '-':
        return 0

    col, row = ep
    r = int(row) - 1
    c = ord(col) - ord("a")
    return 1 + 8 * r + c  # TODO: or the reverse?


def index_to_en_passant(i: int) -> str:
    if i == 0:
        return "-"
    r, c = divmod(i - 1, 8)
    col = chr(ord("a") + c)
    row = str(r + 1)
    return f"{col}{row}"


def row_to_index(row: str) -> int:
    total = 0
    for c in row:
        total = total * len(ALPHABET) + ALPHABET.index(c)
    return total


def index_to_row(i: int) -> str:
    row: list[str] = []
    while i:
        i, r = divmod(i, len(ALPHABET))
        row.append(ALPHABET[r])
    return "".join(reversed(row))
