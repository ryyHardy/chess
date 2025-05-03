"""
Contains data structures defining pieces in chess

This includes piece types, colors, and the piece class

Pieces do not manage their own position. That is the board's job
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class PieceType(Enum):
    PAWN = "p"
    ROOK = "r"
    KNIGHT = "n"
    BISHOP = "b"
    QUEEN = "q"
    KING = "k"


class PieceColor(Enum):
    WHITE = "w"
    BLACK = "b"


@dataclass
class Piece:
    type: PieceType
    color: PieceColor

    def is_king(self) -> bool:
        return self.type.value.lower() == "k"
