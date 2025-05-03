import pytest

from src.engine.fen import (
    FEN_PIECETYPE_MAP,
    InvalidFENError,
    board_from_fen,
    game_from_fen,
    is_valid_fen,
    is_valid_placement_fen,
    piece_from_fen,
)
from src.engine.piece import PieceColor, PieceType


def test_is_valid_placement():
    placement_test_cases = [
        # Valid
        ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR", True),
        ("8/8/8/8/8/8/8/8", True),
        ("r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R", True),
        ("8/8/8/8/8/8/8/P7", True),
        # Too few ranks
        ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP", False),
        # Too many ranks
        ("8/8/8/8/8/8/8/8/8", False),
        # Rank with >8 squares
        ("8/8/8/8/8/8/8/9", False),
        ("8/8/8/8/8/8/8/ppppppppp", False),
        # Rank with <8 squares
        ("8/8/8/8/8/8/8/7", False),
        ("8/8/8/8/8/8/8/P6", False),
        # Invalid characters
        ("8/8/8/8/8/8/8/8*", False),
        ("8/8/8/8/8/8/8/ZZZZZZZZ", False),
        ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPP1/RNBQKBNZ", False),
    ]

    for fen, expected in placement_test_cases:
        assert is_valid_placement_fen(fen) == expected


def test_is_valid_fen():
    fen_test_cases = [
        # Valid FENs
        ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", True),
        ("8/8/8/8/8/8/8/8 b - - 99 42", True),
        ("r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1", True),
        ("rnbq1bnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQ - 3 4", True),
        # Invalid number of fields
        ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0", False),
        ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR", False),
        # Bad piece characters
        ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPZ/RNBQKBNR w KQkq - 0 1", False),
        # Incorrect rank format
        ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPP/RNBQKBNR w KQkq - 0 1", False),  # 7 pawns
        (
            "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNRR w KQkq - 0 1",
            False,
        ),  # Too many pieces in rank
        # Bad active color
        ("8/8/8/8/8/8/8/8 x - - 0 1", False),
        # Bad castling availability
        ("8/8/8/8/8/8/8/8 w KQa - 0 1", False),
        # Bad en passant
        ("8/8/8/8/8/8/8/8 w - e9 0 1", False),
        ("8/8/8/8/8/8/8/8 w - aa 0 1", False),
        # Invalid halfmove and fullmove numbers
        ("8/8/8/8/8/8/8/8 w - - -1 1", False),
        ("8/8/8/8/8/8/8/8 w - - 0 0", False),
        ("8/8/8/8/8/8/8/8 w - - x 1", False),
    ]

    for fen, expected in fen_test_cases:
        assert is_valid_fen(fen) == expected


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

    # Test invalid FENs
    invalid_fens = [
        "invalid",  # Not a valid FEN
        "8/8/8/8/8/8/8",  # Too few ranks
        "8/8/8/8/8/8/8/8/8",  # Too many ranks
        "8/8/8/8/8/8/8/9",  # Invalid number in rank
        "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNZ",  # Invalid piece
    ]

    for fen in invalid_fens:
        with pytest.raises(InvalidFENError):
            board_from_fen(fen)


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
    mid_game_fen = "rnbq1rk1/ppp2ppp/3b1n2/3p4/3P4/2N1PN2/PPP1BPPP/R1BQK2R b KQ e3 2 8"
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
