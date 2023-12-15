from aocd.models import Puzzle

from core import test_and_submit
from util import Matrix

def get_rock_weight(matrix: Matrix, rank: int) -> int:
    return matrix.row_count - rank

def tilt_north(matrix: Matrix) -> None:
    first_free_positions = [0] * matrix.col_count
    for row in range(matrix.row_count):
        for col in range(matrix.col_count):
            current = matrix.get_item(row, col)
            if current == "O":
                matrix.set_item(row, col, ".")
                matrix.set_item(first_free_positions[col], col, "O")
                first_free_positions[col] += 1
            elif current == "#":
                first_free_positions[col] = row+1

def tilt_west(matrix: Matrix) -> None:
    first_free_positions = [0] * matrix.row_count
    for col in range(matrix.col_count):
        for row in range(matrix.row_count):
            current = matrix.get_item(row, col)
            if current == "O":
                matrix.set_item(row, col, ".")
                matrix.set_item(row, first_free_positions[row], "O")
                first_free_positions[row] += 1
            elif current == "#":
                first_free_positions[row] = col+1
                
def tilt_south(matrix: Matrix) -> None:
    first_free_positions = [matrix.row_count-1] * matrix.col_count
    for row in range(matrix.row_count-1, -1, -1):
        for col in range(matrix.col_count):
            current = matrix.get_item(row, col)
            if current == "O":
                matrix.set_item(row, col, ".")
                matrix.set_item(first_free_positions[col], col, "O")
                first_free_positions[col] -= 1
            elif current == "#":
                first_free_positions[col] = row-1

def tilt_east(matrix: Matrix) -> None:
    first_free_positions = [matrix.col_count-1] * matrix.row_count
    for col in range(matrix.col_count-1, -1, -1):
        for row in range(matrix.row_count):
            current = matrix.get_item(row, col)
            if current == "O":
                matrix.set_item(row, col, ".")
                matrix.set_item(row, first_free_positions[row], "O")
                first_free_positions[row] -= 1
            elif current == "#":
                first_free_positions[row] = col-1
                
def spin(matrix: Matrix) -> None:
    tilt_north(matrix)
    tilt_west(matrix)
    tilt_south(matrix)
    tilt_east(matrix)

def solution(input: str) -> tuple[any, any]:
    matrix = Matrix(input)
    iteration = 1000000000
    identical_iteraton = -1
    cache = {}
    for i in range(iteration):
        cache_key = str(matrix.matrix)
        if cache_key in cache:
            matrix.matrix = cache[cache_key]
            identical_iteraton = i+1
            break
        else:
            spin(matrix)
            cache[cache_key] = matrix.matrix

    iteration_left = iteration % identical_iteraton
    for _ in range(iteration_left+1):
        spin(matrix)
        
    result = 0
    for row in range(matrix.row_count):
        for col in range(matrix.col_count):
            if matrix.get_item(row, col) == "O":
                result += get_rock_weight(matrix, row)

    return (None, result)

puzzle = Puzzle(2023, 14)
test_and_submit(puzzle, solution, False)