"""
Contains the move data structure, notation, validators, etc.
"""


class NotationError(Exception):
    """Exception indicating an algebraic notation issue"""

    def __init__(self, message: str):
        super().__init__(message)


def is_valid_square(row: int, col: int) -> bool:
    """Validates square indices

    :param row: Row index. Should be in the range [0,7]
    :type row: int
    :param col: Column index. Should also be in the range [0,7]
    :type col: int
    :return: Whether the square index is valid
    :rtype: bool
    """
    return row in range(8) and col in range(8)


def is_valid_squarename(square_name: str) -> str:
    """Validates square names

    :param square_name: Square name. Should be between 'a1' and 'h8'
    :type square_name: str
    :return: Whether the square name is valid
    :rtype: str
    """
    if len(square_name) != 2:
        return False
    return square_name[0].lower() in "abcdefgh" and square_name[1] in "12345678"


def squarename_to_index(square_name: str) -> tuple[int, int]:
    """Convert a square name to a pair of board indices

    EX: **a1** maps to **(0,0)** and **h8** maps to **(7,7)**

    :param square_name: Square name (may be upper or lowercase)
    :type square_name: str
    :raises InvalidNotationError: If the squarename is not valid algebraic notation
    :return: A tuple of the format (row,col) describing indices to access the square in the board
    :rtype: tuple[int, int]
    """
    if not is_valid_squarename(square_name):
        raise NotationError(
            f"Square name '{square_name}' must be in format 'a1' through 'h8'"
        )

    return int(square_name[1]) - 1, "abcdefgh".find(square_name[0].lower())


def index_to_squarename(row: int, col: int) -> str:
    """Converts board indices to a square name

    :param row: Row index of square on the board
    :type row: int
    :param col: Column index of square on the board
    :type col: int
    :return: Square name string such as "e6" or "h3"
    :rtype: str
    """
    if not is_valid_square(row, col):
        raise NotationError(
            f"Square index (row={row},col={col}) cannot be converted to square name"
        )
    return f"{'abcdefgh'[col]}{row + 1}"
