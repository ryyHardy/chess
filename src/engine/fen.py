"""
Contains FEN (Forsyth-Edwards Notation) related utilities such as parsers and validators
"""

import re

from .board import ChessBoard
from .chess import ChessGame
from .move import squarename_to_index
from .piece import Piece, PieceColor, PieceType

STARTING_FEN_SHORT = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
STARTING_FEN_LONG = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

FEN_PIECETYPE_MAP: dict[str, PieceType] = {
    "p": PieceType.PAWN,
    "r": PieceType.ROOK,
    "n": PieceType.KNIGHT,
    "b": PieceType.BISHOP,
    "q": PieceType.QUEEN,
    "k": PieceType.KING,
}


class InvalidFENError(Exception):
    """Exception indicating an invalid FEN string"""

    def __init__(self, fen: str, reason: str = ""):
        self.message = f"Invalid FEN string: '{fen}'"
        if reason:
            self.message += f"\n\tReason: {reason}"
        super().__init__(self.message)


def is_valid_fen(fen: str) -> bool:
    """Fully validates a FEN string (for all practical purposes) based on the following rules:

    **"Format" Rules**
    1. It must have 6 fields separated by spaces: piece placement, active color, castling rights, en passant square, halfmove count, fullmove count.
    2. The piece placement field needs exactly 8 "rows", or strings separated by '/'.
        - Each row must consist of a combination of digits and piece characters.
        - Valid piece characters are 'prnbqkPRNBQK'. Valid digits are 1-8.
        - For each row, total of digits in the row + number of piece characters in the row == 8.
    3. Active color field must be either 'w' or 'b'.
    4. Castling rights field must be a combination of 'K', 'Q', 'k', and 'q' characters, or the field should be '-' to indicate no rights.
    5. En passant square field is either '-' or a valid square on rank 3 or 6 (a3-h3, a6-h6).
    6. Board boundaries are respected throughout (no overflow past 8x8).
    7. Halfmove and fullmove fields must be non-negaitve integers.
    8. No extra or missing characters in any field.

    **"Semantic" Rules**
    1. There must be exactly one white king and one black king
    2. For each castling right, the relevant king and rook must be on the correct squares to perform it.
    3. If an en passant square is specified, the opposing pawns must be on the correct squares to perform it.

    :param fen: A FEN string consisting of all 6 fields. *EX: 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1' for starting position*
    :type fen: str

    :return: Whether the FEN string is valid according to the rules described
    :rtype: bool
    """
    try:
        parts = fen.strip().split()
        if len(parts) != 6:
            return False

        (
            piece_placement,
            active_color,
            castling_rights,
            en_passant,
            halfmove_clock,
            fullmove_number,
        ) = parts

        if not re.match(r"^[prnbqkPRNBQK1-8/]+$", piece_placement):
            return False

        if active_color not in ("w", "b"):
            return False

        if castling_rights != "-" and not re.match(r"^[KQkq]+$", castling_rights):
            return False

        if en_passant != "-" and not re.match(r"^[a-h][36]$", en_passant):
            return False

        if not halfmove_clock.isdigit() or not fullmove_number.isdigit():
            return False

        # Create board using new coordinate logic: row 0 = rank 1, row 7 = rank 8
        board = [["" for _ in range(8)] for _ in range(8)]
        rows = piece_placement.split("/")
        if len(rows) != 8:
            return False

        for fen_row_index, row in enumerate(rows):
            board_row = 7 - fen_row_index  # Rank 8 is row 7, Rank 1 is row 0
            col = 0
            for ch in row:
                if ch.isdigit():
                    col += int(ch)
                elif ch in "prnbqkPRNBQK":
                    if col >= 8:
                        return False
                    board[board_row][col] = ch
                    col += 1
                else:
                    return False
            if col != 8:
                return False

        # Count kings
        white_kings = sum(row.count("K") for row in board)
        black_kings = sum(row.count("k") for row in board)
        if white_kings != 1 or black_kings != 1:
            return False

        # Correct castling square mappings in new coordinate system
        king_positions = {"K": (0, 4), "Q": (0, 4), "k": (7, 4), "q": (7, 4)}
        rook_positions = {"K": (0, 7), "Q": (0, 0), "k": (7, 7), "q": (7, 0)}

        if castling_rights != "-":
            for flag in castling_rights:
                if flag not in "KQkq":
                    return False

                k_row, k_col = king_positions[flag]
                r_row, r_col = rook_positions[flag]
                expected_king = "K" if flag.isupper() else "k"
                expected_rook = "R" if flag.isupper() else "r"

                if (
                    board[k_row][k_col] != expected_king
                    or board[r_row][r_col] != expected_rook
                ):
                    return False

        if en_passant != "-":
            file = ord(en_passant[0]) - ord("a")
            rank = int(en_passant[1])
            row = rank - 1  # Rank 1 = row 0

            if active_color == "w":
                # White to move → Black must have just double-pushed
                # Look for black pawn on rank 5 that moved from rank 7
                if rank != 6 or board[row][file] != "p":
                    return False
            elif active_color == "b":
                # Black to move → White must have just double-pushed
                # Look for white pawn on rank 4 that moved from rank 2
                if rank != 3 or board[row][file] != "P":
                    return False
            else:
                return False

        return True

    except Exception:
        return False


def piece_from_fen(fen_symbol: str) -> Piece:
    """Create a piece from a FEN symbol

    :param fen_symbol: FEN symbol for the piece. Should be one of (p,r,n,b,q,k), upper or lowercase
    :type fen_symbol: str
    :raises InvalidFENError: If the symbol is not a valid FEN symbol for a piece
    :return: The piece corresponding to the provided FEN symbol
    :rtype: Piece
    """
    try:
        color = PieceColor.WHITE if fen_symbol.isupper() else PieceColor.BLACK
        piece_type = FEN_PIECETYPE_MAP[fen_symbol.lower()]
        return Piece(piece_type, color)
    except KeyError:
        raise InvalidFENError(
            fen_symbol,
            "Not a valid FEN symbol for a piece. Should be one of (p,r,n,b,q,k), upper or lowercase",
        )


def board_from_fen(piece_placement_fen: str) -> ChessBoard:
    """Create a board from the piece placement field of a FEN string with the ASSUMPTION that it is valid

    :param piece_placement_fen: FEN string consisting **only** of the piece placement field
    :type piece_placement_fen: str
    :return: The board object corresponding to the provided FEN
    :rtype: ChessBoard
    """

    board = ChessBoard()
    row, col = 7, 0
    for c in piece_placement_fen:
        if c == "/":
            row -= 1
            col = 0
        elif c.isdigit():
            col += int(c)
        else:
            board.set_piece(piece_from_fen(c), row, col)
            col += 1
    return board


def game_from_fen(fen: str) -> ChessGame:
    """Create a game instance from a full FEN string

    :param fen: A FULL FEN string with all the fields. For example, the FEN for the starting position is ""
    :type fen: str
    :raises InvalidFENError: If the FEN is invalid
    :return: A chess game instance loaded from the FEN
    :rtype: ChessGame
    """
    if not is_valid_fen(fen):
        raise InvalidFENError(fen, "FEN cannot be used to create game")

    game = ChessGame()
    fields = fen.split(" ")

    game.board = board_from_fen(fields[0])

    game.active_color = PieceColor.WHITE if fields[1] == "w" else PieceColor.BLACK

    game.white_castle_kingside = "K" in fields[2]
    game.white_castle_queenside = "Q" in fields[2]
    game.black_castle_kingside = "k" in fields[2]
    game.black_castle_queenside = "q" in fields[2]

    game.en_passant_square = (
        None if fields[3] == "-" else squarename_to_index(fields[3])
    )

    game.halfmove_counter = int(fields[4])
    game.fullmove_counter = int(fields[5])

    return game
