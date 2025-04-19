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
        """Creates a piece matching a FEN symbol

        :param fen: The FEN symbol determining the type and color of the piece
        :type fen: str
        :return: The piece corresponding to the provided FEN symbol
        :rtype: Piece
        :raises ValueError: If the FEN symbol is not one of "prnbqkPRNBQK"
        """
        try:
            color = PieceColor.WHITE if fen.isupper() else PieceColor.BLACK
            piece_type = FEN_MAP[fen.lower()]
            return Piece(piece_type, color)
        except KeyError:
            raise ValueError(f"Invalid FEN symbol '{fen}' used to create piece")

    def is_king(self) -> bool:
        return self.type.value.lower() == "k"
