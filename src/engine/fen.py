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


def is_valid_placement_fen(fen_piece_placement: str) -> bool:
    """Checks if the piece placement field of a FEN string is valid

    :param fen: FEN consisting **only** of the piece placement field
    :type fen: str
    :return: Whether the piece placement field is valid
    :rtype: bool
    """
    ranks = fen_piece_placement.strip().split("/")
    if len(ranks) != 8:
        return False

    valid_pieces = set("pnbrqkPNBRQK")

    for rank in ranks:
        total = 0
        for char in rank:
            if char.isdigit():
                total += int(char)
            elif char in valid_pieces:
                total += 1
            else:
                return False
        if total != 8:
            return False

    return True


def is_valid_fen(fen: str) -> bool:
    """Checks if a FEN string meets the format requriements of FEN. Does **not** check legality

    :param fen: The FEN string to validate
    :type fen: str
    :return: Whehter the FEN string is valid (format-wise)
    :rtype: bool
    """
    fields = fen.strip().split()
    if len(fields) != 6:
        return False

    piece_placement, active_color, castling, en_passant, halfmove, fullmove = fields

    # Validate piece placement
    if not is_valid_placement_fen(piece_placement):
        return False

    # Validate active color
    if active_color not in ("w", "b"):
        return False

    # Validate castling availability
    if castling != "-" and not re.fullmatch(r"[KQkq]+", castling):
        return False

    # Validate en passant square
    if en_passant != "-" and not re.fullmatch(r"^[a-h][36]$", en_passant):
        return False

    # Validate halfmove clock
    if not halfmove.isdigit() or int(halfmove) < 0:
        return False

    # Validate fullmove number
    if not fullmove.isdigit() or int(fullmove) < 1:
        return False

    return True


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
    """Create a board from the piece placement field of a FEN string

    :param piece_placement_fen: FEN string consisting **only** of the piece placement field
    :type piece_placement_fen: str
    :raises InvalidFENError: If piece placement field is invalid
    :return: The board object corresponding to the provided FEN
    :rtype: ChessBoard
    """
    if not is_valid_placement_fen(piece_placement_fen):
        raise InvalidFENError(piece_placement_fen, "Invalid piece placement field")

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
        raise InvalidFENError(fen, "Invalid full FEN")

    game = ChessGame()
    fields = fen.split(" ")

    try:
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
    except Exception as e:
        raise InvalidFENError(fen, str(e))
