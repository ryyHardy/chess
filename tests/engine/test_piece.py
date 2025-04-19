import pytest

from src.engine.piece import FEN_MAP, Piece, PieceColor, PieceType

FEN_SYMBOLS = "prnbqkPRNBQK"


def test_from_fen():
    # Use all valid FEN piece symbols and check if the generated pieces are correct
    pieces = [Piece.from_fen_symbol(sym) for sym in FEN_SYMBOLS]

    for i, piece in enumerate(pieces):
        correct_color = (
            PieceColor.WHITE if FEN_SYMBOLS[i].isupper() else PieceColor.BLACK
        )
        correct_type = FEN_MAP[FEN_SYMBOLS[i].lower()]

        assert piece.type == correct_type
        assert piece.color == correct_color

    # Use an invalid FEN piece symbol and ensure it raises a ValueError
    with pytest.raises(ValueError) as excinfo:
        Piece.from_fen_symbol("Z")
    assert "Invalid FEN symbol" in str(excinfo.value)


def test_is_king():
    pieces = [Piece.from_fen_symbol(sym) for sym in FEN_SYMBOLS]
    for piece in pieces:
        if piece.type == PieceType.KING:
            assert piece.is_king()
        else:
            assert not piece.is_king()
