from aocd.models import Puzzle

from core import test_and_submit
from util import Matrix

def solution(input: str) -> tuple[any, any]:
    matrix = Matrix(input)
    empty_rows = set(range(matrix.row_count))
    empty_cols = set(range(matrix.col_count))
    galaxies = set()
    paths = {}

    for row in range(matrix.row_count):
        for col in range(matrix.col_count):
            if matrix.get_item(row, col) == "#":
                empty_rows.discard(row)
                empty_cols.discard(col)
                
                galaxy = (row, col)
                for existing_galaxy in galaxies:
                    paths[(existing_galaxy, galaxy)] = 0
                galaxies.add(galaxy)
    
    for pair in paths:
        first, second = pair
        row_range = set(range(first[0], second[0])) if first[0] < second[0] else set(range(second[0], first[0]))
        row_duplicates = row_range.intersection(empty_rows)
        row_diff = len(row_range) + len(row_duplicates)

        col_range = set(range(first[1], second[1])) if first[1] < second[1] else set(range(second[1], first[1]))
        col_duplicates = col_range.intersection(empty_cols)
        col_diff = len(col_range) + len(col_duplicates)
        
        paths[pair] = row_diff + col_diff
        
    result = sum(paths.values())
    return (result, None)

puzzle = Puzzle(2023, 11)
test_and_submit(puzzle, solution, False)