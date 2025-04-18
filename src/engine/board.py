from dataclasses import dataclass, field

from piece import Piece, PieceColor, PieceType


def create_empty_board() -> list[list[Piece | None]]:
    return [[None for _ in range(8)] for _ in range(8)]


@dataclass
class Board:
    squares: list[list[Piece | None]] = field(default_factory=create_empty_board)


b = Board()
print(b.squares)
