from aocd.models import Puzzle

from core import test_and_submit
from util import Matrix

def get_rock_weight(matrix: Matrix, rank: int) -> int:
    return matrix.row_count - rank

def solution(input: str) -> tuple[any, any]:
    matrix = Matrix(input)
    # matrix.print()
    # print()
    result = 0
    first_free_positions = [0] * matrix.col_count
    for row in range(matrix.row_count):
        for col in range(matrix.col_count):
            current = matrix.get_item(row, col)
            if current == "O":
                matrix.set_item(row, col, ".")
                matrix.set_item(first_free_positions[col], col, "O")
                result += get_rock_weight(matrix, first_free_positions[col])
                first_free_positions[col] += 1
            elif current == "#":
                first_free_positions[col] = row+1
                
        # matrix.print()
        # print()
            
    return (result, None)

puzzle = Puzzle(2023, 14)
test_and_submit(puzzle, solution, False)