"""
Contains the data structure for the chess board itself

The chess board is responsible for managing piece positions

The board is indexed via row and column indices (row,col), where (0,0) is a1 and (7,7) is h8
"""

from dataclasses import dataclass, field

from .piece import Piece, PieceColor


def create_empty_squares() -> list[list[Piece | None]]:
    """Creates an empty 8x8 grid to pass to the board

    :return: An empty 8x8 grid that can be filled with pieces
    :rtype: list[list[Piece | None]]
    """
    return [[None for _ in range(8)] for _ in range(8)]


@dataclass
class ChessBoard:
    squares: list[list[Piece | None]] = field(default_factory=create_empty_squares)

    def get_square(self, row: int, col: int) -> Piece | None:
        return self.squares[row][col]

    def set_piece(self, piece: Piece | None, row: int, col: int):
        self.squares[row][col] = piece

    def move_piece(self, start_row: int, start_col: int, end_row: int, end_col: int):
        """Move a piece from a start square to an end square

        :param start_row: Row index of the start square
        :type start_row: int
        :param start_col: Column index of the start square
        :type start_col: int
        :param end_row: Row index of the end square
        :type end_row: int
        :param end_col: Column index of the end square
        :type end_col: int
        """
        piece = self.squares[start_row][start_col]
        if piece is not None:
            self.squares[end_row][end_col] = piece

    def is_empty(self, row: int, col: int):
        return self.squares[row][col] is None

    def in_bounds(self, row: int, col: int):
        return row in range(8) and col in range(8)

    def find_king(self, color: PieceColor) -> tuple[int, int]:
        """Find the king's square (of the provided color)

        :param color: Which color king to find
        :type color: PieceColor
        :return: A [row,col] tuple representing the king's location
        :rtype: tuple[int, int]
        """
        for row in range(8):
            for col in range(8):
                piece = self.squares[row][col]
                if piece and piece.is_king() and piece.color == color:
                    return (row, col)
