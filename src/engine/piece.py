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


FEN_MAP: dict[str, PieceType] = {
    "p": PieceType.PAWN,
    "r": PieceType.ROOK,
    "n": PieceType.KNIGHT,
    "b": PieceType.BISHOP,
    "q": PieceType.QUEEN,
    "k": PieceType.KING,
}


class PieceColor(Enum):
    WHITE = "w"
    BLACK = "b"


@dataclass
class Piece:
    type: PieceType
    color: PieceColor

    @staticmethod
    def from_fen_symbol(fen: str) -> Piece:
        """Creates a Piece object from a FEN symbol

        :param fen: The FEN symbol. Case determines color and letter determines type. Valid letters are p, r, n, b, q, and k
        :type fen: str
        :return: A Piece object with its color and type set according to the FEN symbol
        :rtype: Piece
        """
        color = PieceColor.WHITE if fen.isupper() else PieceColor.BLACK
        piece_type = FEN_MAP[fen.lower()]

        return Piece(piece_type, color)

    def is_king(self) -> bool:
        return self.type.value.lower() == "k"
