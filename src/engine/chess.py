"""
Contains a class for the chess game

A chess game encapsulates the board and game state, providing an interface to play the game
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .board import ChessBoard
from .piece import PieceColor


@dataclass
class ChessGame:
    board: ChessBoard = field(default_factory=ChessBoard)

    active_color: PieceColor = PieceColor.WHITE

    white_castle_kingside: bool = True
    white_castle_queenside: bool = True
    black_castle_kingside: bool = True
    black_castle_queenside: bool = True

    en_passant_square: tuple[int, int] | None = None

    halfmove_counter: int = 0
    fullmove_counter: int = 1

    def make_move(self, move: str) -> bool:
        """Make a move in the game

        :param move: Algebraic notation for the move
        :type move: str
        :return: Whether the move is legal
        :rtype: bool
        """
        pass

    def legal_moves(self) -> list[str]:
        """Return a list of all current legal moves

        :return: A list of strings (algebraic notation) representing all current legal moves
        :rtype: list[str]
        """
        pass

    def current_turn(self) -> str:
        """Get the current turn

        :return: "white" or "black"
        :rtype: str
        """
        pass

    def in_check(self) -> bool:
        """Determine whether the current player is in check

        :return: Whether the current player is in check
        :rtype: bool
        """
        pass

    def is_checkmate(self) -> bool:
        """Determine whether the current player is checkamted

        :return: Whether the current player is checkmated
        :rtype: bool
        """
        pass

    def is_stalemate(self) -> bool:
        """Determine whether the game is in stalemate

        :return: Whether the game is in stalemate
        :rtype: bool
        """

    def get_fen(self) -> str:
        """Create a FEN string for the current position

        :return: _description_
        :rtype: str
        """
        pass

    def undo_move(self):
        """Undoes the previous move"""
        pass
