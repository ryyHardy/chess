from src.engine.board import ChessBoard, create_empty_squares


def test_create_empty_squares():
    empty = [[None for _ in range(8)] for _ in range(8)]
    assert empty == create_empty_squares()


def test_construct():
    # Test that ChessBoard is using create_empty_squares as a default factory
    empty_board = ChessBoard()
    empty_squares = create_empty_squares()
    assert empty_board.squares == empty_squares
