"""Puts matrices into Reduced Row Echelon Form"""
import enum
from functools import reduce
from tkinter.tix import Form
from common import *

FormattedRow = list[Fraction | int]
FormattedMatrix = list[FormattedRow]


def _print_matrix(matrix: FormattedMatrix, format: bool=False) -> None:
    matrix = [[(i if (not isinstance(i, Fraction) or i.denominator != 1) else i.numerator) for i in row ]for row in matrix]
    print(*matrix, sep="\n", end="\n" * 3)

def _reduce_pos_to_zero(pos: int, r0: FormattedRow, r1: FormattedRow) -> FormattedRow:
    """Takes two rows and uses them to reduce a term at position `pos` to 0"""
    # Force the two rows to have a common denominator
    minuend = (r0[pos] * i for i in r1)
    subtrahend = (r1[pos] * i for i in r0)
    # Subtract from one another
    return [m - s for m, s in zip(minuend, subtrahend)]

def divide_by_diagonal_coefficient(matrix: FormattedMatrix) -> FormattedMatrix:
    """Divides nth rows of a matrix by its coefficient at column n. Ignores coefficients of 0.

    For example,
        | A B C |                  | 1   B/A C/A |
        | E F G |     results in   | E/F   1 G/F |
    
    This is helpful with obtaining row-echelon form, as
        | A B C D |                | 1   B/A C/A D/A |
        | 0 E F G |   results in   | 0   1   F/E G/E |
        | 0 0 H I |                | 0   0   1   I/H |
    """
    matrix = [[Fraction(i) / row[pos] for i in row] for pos, row in enumerate(matrix) if row[pos]]
    return matrix

def reduced_row_echelon(matrix: FormattedMatrix) -> FormattedMatrix:
    """Formats a matrix into Reduced Row Echelon Form"""
    # TODO: Generalize beyond 3x4 matrices
    try:
        assert 3 == len(matrix)
        assert all(len(row) == 4 for row in matrix)
    except AssertionError as e:
        raise ValueError("Matrix must be be of dimensions 3x4") from e
    
    # If 0s occur at the top, it *will* cause issues
    matrix.sort(key=lambda i: -abs(i[0]))
    _print_matrix(matrix)

    # Eliminate first column of zeros
    matrix[1] = _reduce_pos_to_zero(0, matrix[0], matrix[1])
    matrix[2] = _reduce_pos_to_zero(0, matrix[0], matrix[2])
    assert matrix[1][0] == 0
    assert matrix[2][0] == 0
    _print_matrix(matrix)

    # Repeat for last row, second column
    matrix[2] = _reduce_pos_to_zero(1, matrix[1], matrix[2])
    assert matrix[2][1] == 0
    _print_matrix(matrix)

    # Ensure first non-zero coefficient is equal to 1
    matrix = divide_by_diagonal_coefficient(matrix)
    _print_matrix(matrix)
    # Eliminate remaining non-diagonal zeros
    matrix[0] = _reduce_pos_to_zero(1, matrix[0], matrix[1])
    matrix[0] = _reduce_pos_to_zero(2, matrix[0], matrix[2])
    matrix[1] = _reduce_pos_to_zero(2, matrix[2], matrix[1])
    # for reasons I'm too lazy to comprehend, `2, matrix[1], matrix[2]` yields a negative output
    _print_matrix(matrix)

    return matrix


def display_rre_steps(_input: list[list[num]] | list[list[str]] | str | None = None) -> FormattedMatrix:
    if not _input:
        _input = input("Matrix?")
    if isinstance(_input, str):
        _input = [row.split(",") for row in _input.split(";")]
    resp: FormattedMatrix = [[Fraction(i) for i in row] for row in _input]
    return reduced_row_echelon(resp)


rre = display_rre_steps
RRE = display_rre_steps
