import pytest

from src.engine.fen import (
    FEN_PIECETYPE_MAP,
    InvalidFENError,
    board_from_fen,
    game_from_fen,
    is_valid_fen,
    piece_from_fen,
)
from src.engine.piece import PieceColor, PieceType


@pytest.mark.parametrize(
    "fen",
    [
        # Valid FENs
        "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",  # starting position
        "4k3/8/8/8/8/8/8/4K3 w - - 0 1",  # minimal kings only
        "r3k2r/pppppppp/8/8/8/8/PPPPPPPP/R3K2R w KQkq - 0 1",  # castling setup
        "4k3/8/8/8/8/8/8/R3K2R w KQ - 0 1",  # valid white castling
        "r3k3/8/8/8/8/8/8/4K3 b q - 0 1",  # king moved, no castling
    ],
)
def test_valid_fens(fen):
    assert is_valid_fen(fen)


@pytest.mark.parametrize(
    "fen",
    [
        # Invalid due to format issues
        "8/8/8/8/8/8/8 w - - 0 1",  # only 7 rows
        "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/ w KQkq - 0 1",  # missing 8th row data
        "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPP/RNBQKBNR w KQkq - 0 1",  # bad row length
        "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBN w KQkq - 0 1",  # missing square
        "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNRX w KQkq - 0 1",  # invalid piece char
        "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w P - 0 1",  # invalid castling rights
        "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR x KQkq - 0 1",  # invalid active color
        "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq z9 0 1",  # invalid en passant square
        "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - -1 1",  # negative halfmove
        "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 -5",  # negative fullmove
    ],
)
def test_invalid_format_fens(fen):
    assert not is_valid_fen(fen)


@pytest.mark.parametrize(
    "fen",
    [
        # Invalid because of king count
        "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1".replace(
            "K", ""
        ),  # missing white king
        "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKKBNR w KQkq - 0 1",  # extra white king
    ],
)
def test_invalid_king_count(fen):
    assert not is_valid_fen(fen)


@pytest.mark.parametrize(
    "fen",
    [
        # Invalid castling positions
        "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/4K3 w K - 0 1",  # claims kingside but no h1 rook
        "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/4K3 w Q - 0 1",  # claims queenside but no a1 rook
        "4k3/pppppppp/8/8/8/8/PPPPPPPP/R3K2R w k - 0 1",  # claims black kingside but black rook moved
    ],
)
def test_invalid_castling_rights(fen):
    assert not is_valid_fen(fen)


@pytest.mark.parametrize(
    "fen",
    [
        # Invalid en passant (no pawn to capture)
        "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w - a6 0 1",  # no white pawn to capture on a5
        "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR b - h3 0 1",  # no black pawn to capture on h4
    ],
)
def test_invalid_en_passant(fen):
    assert not is_valid_fen(fen)


def test_piece_from_fen():
    valid_fens = "prnbqkPRNBQK"
    for symbol in valid_fens:
        p = piece_from_fen(symbol)
        expected_color = PieceColor.WHITE if symbol.isupper() else PieceColor.BLACK
        assert p.color == expected_color
        expected_type = FEN_PIECETYPE_MAP[symbol.lower()]
        assert p.type == expected_type

    invalid_fens = ("$", "", "pK")
    for symbol in invalid_fens:
        with pytest.raises(InvalidFENError):
            p = piece_from_fen(symbol)


def test_board_from_fen():
    # Test empty board
    empty_fen = "8/8/8/8/8/8/8/8"
    empty_board = board_from_fen(empty_fen)
    for row in range(8):
        for col in range(8):
            assert empty_board.get_square(row, col) is None

    # Test starting position
    start_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
    start_board = board_from_fen(start_fen)

    # Check black back rank
    back_rank = "rnbqkbnr"
    for col, symbol in enumerate(back_rank):
        piece = start_board.get_square(7, col)
        assert piece is not None
        assert piece.color == PieceColor.BLACK
        assert piece.type == FEN_PIECETYPE_MAP[symbol.lower()]

    # Check black pawns
    for col in range(8):
        piece = start_board.get_square(6, col)
        assert piece is not None
        assert piece.color == PieceColor.BLACK
        assert piece.type == PieceType.PAWN

    # Check empty middle ranks
    for row in range(2, 6):
        for col in range(8):
            assert start_board.get_square(row, col) is None

    # Check white pawns
    for col in range(8):
        piece = start_board.get_square(1, col)
        assert piece is not None
        assert piece.color == PieceColor.WHITE
        assert piece.type == PieceType.PAWN

    # Check white back rank
    back_rank = "RNBQKBNR"
    for col, symbol in enumerate(back_rank):
        piece = start_board.get_square(0, col)
        assert piece is not None
        assert piece.color == PieceColor.WHITE
        assert piece.type == FEN_PIECETYPE_MAP[symbol.lower()]


def test_game_from_fen():
    # Test initial position
    start_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    game = game_from_fen(start_fen)
    assert game.white_castle_kingside is True
    assert game.white_castle_queenside is True
    assert game.black_castle_kingside is True
    assert game.black_castle_queenside is True
    assert game.en_passant_square is None
    assert game.halfmove_counter == 0
    assert game.fullmove_counter == 1

    # Test position with specific castling rights and en passant
    mid_game_fen = "rnbq1rk1/ppp2ppp/3b1n2/3p4/3P4/2N1PN2/PPP1BPPP/R3K2R b KQ e3 2 8"
    game = game_from_fen(mid_game_fen)
    assert game.white_castle_kingside is True
    assert game.white_castle_queenside is True
    assert game.black_castle_kingside is False
    assert game.black_castle_queenside is False
    assert game.en_passant_square == (2, 4)  # e3 square
    assert game.halfmove_counter == 2
    assert game.fullmove_counter == 8

    # Test position with no castling rights
    endgame_fen = "4k3/8/8/8/8/8/8/4K3 w - - 10 50"
    game = game_from_fen(endgame_fen)
    assert game.white_castle_kingside is False
    assert game.white_castle_queenside is False
    assert game.black_castle_kingside is False
    assert game.black_castle_queenside is False
    assert game.en_passant_square is None
    assert game.halfmove_counter == 10
    assert game.fullmove_counter == 50

    # Test invalid FENs
    invalid_fens = [
        "invalid",  # Not a valid FEN
        "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq -",  # Missing fields
        "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0",  # Missing fullmove
        "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkx - 0 1",  # Invalid castling
        "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq e9 0 1",  # Invalid en passant
    ]

    for fen in invalid_fens:
        with pytest.raises(InvalidFENError):
            game_from_fen(fen)
