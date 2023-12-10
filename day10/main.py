from aocd.models import Puzzle

from core import test_and_submit
from util import Matrix

valid_connections = {
    "up" : { "|", "7", "F" },
    "down" : { "|", "L", "J" },
    "left" : { "-", "L", "F" },
    "right" : { "-", "J", "7" },
}

def get_move(matrix: Matrix, direction: str, position: tuple[int,int]) -> tuple[int, int] | None:
    if matrix.get_item(position[0], position[1]) in valid_connections[direction]:
        return position
    else:
        return None

def get_valid_moves(matrix: Matrix, pipe: str, position: tuple[int,int]) -> list[tuple[int,int]]:
    up = get_move(matrix, "up", (position[0] - 1, position[1]))
    down = get_move(matrix, "down", (position[0] + 1, position[1]))
    left = get_move(matrix, "left", (position[0], position[1] - 1))
    right = get_move(matrix, "right", (position[0], position[1] + 1))
    possible_moves = {
        "S": [up, down, left, right],
        "|": [up, down],
        "-": [left, right],
        "L": [up, right],
        "J": [up, left],
        "7": [down, left],
        "F": [down, right]
    }
    return [x for x in possible_moves[pipe] if x is not None]
    
def get_connecting_pipe(matrix: Matrix, position: tuple[int,int], loop: set[tuple[int,int]]) -> tuple[int,int] | None:
    if not position:
        return None
        
    pipe = matrix.get_item(position[0], position[1])
    next_pipe = next((p for p in get_valid_moves(matrix, pipe, position) if p and p not in loop), None)
    if next_pipe:
        loop.add(next_pipe)
        
    return next_pipe

def find_start(matrix: Matrix) -> tuple[int,int]:
    for row in range(matrix.row_count):
        for col in range(matrix.col_count):
            if matrix.get_item(row, col) == "S":
                return (row, col)
            
def is_enclosed(matrix: Matrix, loop: set[tuple[int,int]], row: int, col: int) -> bool:
    current = (row, col)
    #if position is part of the loop, it's instant no
    if (row, col) in loop:
        return False

    count = 0
    while current[0] >= 0 and current[0] < matrix.row_count and current[1] >= 0 and current[1] < matrix.col_count:
        #we pick e.g. left
        current = (current[0], current[1]-1)
        #we need an odd number of horizontal loop elements to cross
        #not 7 or F, because we check only what has no upper half
        if current in loop and matrix.get_item(current[0], current[1]) in {"|", "J", "L"}:
            count += 1
            
    return count % 2 == 1

def get_s(matrix: Matrix, starting_points: list[tuple[int,int]]) -> str:
    starting_points.sort()
    first, second = starting_points[0], starting_points[1]
    if first[0] == second[0]: return "-"
    if first[1] == second[1]: return "|"
    if first[0] < second[0] and first[1] < second[1]: return "7" 
    if first[0] < second[0] and first[1] > second[1]: return "F" 
    if first[0] > second[0] and first[1] < second[1]: return "J" 
    if first[0] > second[0] and first[1] > second[1]: return "L" 

def solution(input: str) -> tuple[any, any]:
    matrix = Matrix(input)
    start = find_start(matrix)
    loop = { start }
    pipes = [get_connecting_pipe(matrix, start, loop), get_connecting_pipe(matrix, start, loop)]
    start_real_pipe = get_s(matrix, pipes)
    
    while any(pipes):
        for i in range(len(pipes)):
            pipes[i] = get_connecting_pipe(matrix, pipes[i], loop)
    
    matrix.matrix[start[0]][start[1]] = start_real_pipe

    enclosed_tiles = 0
    #we have the loop now, let's check the area
    #if performance would be bad, we can limit our search to the rectangle of the outer loop then probably
    for row in range(matrix.row_count):
        for col in range(matrix.col_count):
            if is_enclosed(matrix, loop, row, col):
                enclosed_tiles += 1
                
    return (None, enclosed_tiles)

puzzle = Puzzle(2023, 10)
test_and_submit(puzzle, solution, False)