from aocd.models import Puzzle

from core import test_and_submit
from util import Matrix

def get_move(matrix: Matrix, direction: str, position: tuple[int,int]) -> tuple[int, int] | None:
    valid_connections = {
        "up" : { "|", "7", "F" },
        "down" : { "|", "L", "J" },
        "left" : { "-", "L", "F" },
        "right" : { "-", "J", "7" },
    }
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
            
def solution(input: str) -> tuple[any, any]:
    matrix = Matrix(input)
    start = find_start(matrix)
    loop = { start }
    pipes = [get_connecting_pipe(matrix, start, loop), get_connecting_pipe(matrix, start, loop)]
    max_steps = 0
    while any(pipes):
        for i in range(len(pipes)):
            pipes[i] = get_connecting_pipe(matrix, pipes[i], loop)
            
        max_steps += 1
        
    return (max_steps, None)

puzzle = Puzzle(2023, 10)
test_and_submit(puzzle, solution, False)