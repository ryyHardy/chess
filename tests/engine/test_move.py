import pytest

from src.engine.move import (
    NotationError,
    index_to_squarename,
    is_valid_square,
    is_valid_squarename,
    squarename_to_index,
)


def test_is_valid_squarename():
    # Test all possible valid squares (and ensure case insensitivity)
    for letter in "aBcDeFgH":
        for number in "12345678":
            assert is_valid_squarename(letter + number), (
                f"Square {letter}{number} should be valid"
            )

    # Test invalid squares
    invalid_squares = [
        "1a",  # wrong order
        "11",  # no letter
        "a",  # too short
        "1",  # too short
        "$$",  # invalid chars
        "$",  # invalid char
        "i1",  # invalid letter
        "",  # empty string
        "a9",  # invalid number
        "h0",  # invalid number
        "a1b",  # too long
        " a1",  # leading space
        "a1 ",  # trailing space
    ]

    for square in invalid_squares:
        assert not is_valid_squarename(square), f"Square '{square}' should be invalid"


def test_squarename_to_index():
    # Confirm that coordinate system is correct, and that case is ignored
    corners = [("a1", (0, 0)), ("A8", (7, 0)), ("H1", (0, 7)), ("h8", (7, 7))]

    for square, expected in corners:
        assert squarename_to_index(square) == expected

    invalid_names = ["1a", "h9", "i8", "ee", "44", "$", "$$$"]
    for sqr in invalid_names:
        with pytest.raises(NotationError):
            squarename_to_index(sqr)


def test_index_to_squarename():
    # Confirm that coordinate system is correct
    corners = [((0, 0), "a1"), ((7, 0), "a8"), ((0, 7), "h1"), ((7, 7), "h8")]

    for (row, col), expected in corners:
        assert index_to_squarename(row, col) == expected

    invalid_squares = [(-1, 0), (8, 0), (0, -1), (0, 8), (-1, -1), (8, 8)]
    for row, col in invalid_squares:
        with pytest.raises(NotationError):
            index_to_squarename(row, col)
