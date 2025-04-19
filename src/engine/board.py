from dataclasses import dataclass, field

from .piece import Piece, PieceColor, PieceType


def create_empty_squares() -> list[list[Piece | None]]:
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

    @staticmethod
    def from_fen(fen: str = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"):
        board = ChessBoard()
        row, col = 7, 0
        for c in fen.split()[0]:
            if c == "/":
                row -= 1
                col = 0
            elif c.isdigit():
                col += int(c)
            else:
                board.set_piece(Piece.from_fen_symbol(c), row, col)
                col += 1
        return board
