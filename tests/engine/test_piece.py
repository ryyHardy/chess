from src.engine.fen import piece_from_fen
from src.engine.piece import Piece, PieceType

FEN_SYMBOLS = "prnbqkPRNBQK"


def test_is_king():
    pieces = [piece_from_fen(sym) for sym in FEN_SYMBOLS]
    for piece in pieces:
        if piece.type == PieceType.KING:
            assert piece.is_king()
        else:
            assert not piece.is_king()
        assert not piece.has_moved
