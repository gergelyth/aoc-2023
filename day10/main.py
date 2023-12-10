from aocd.models import Puzzle
from typing import Callable

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
            
def is_there_odd_loop_in_direction(matrix: Matrix, loop: set[tuple[int,int]], cross_symbols: set[str], current: tuple[int,int], move: Callable[[tuple[int,int]], tuple[int,int]]) -> bool:
    count = 0
    while current[0] >= 0 and current[0] < matrix.row_count and current[1] >= 0 and current[1] < matrix.col_count:
        current = move(current)
        if current in loop and matrix.get_item(current[0], current[1]) in {"|", "J", "L"}:
            count += 1

    return count % 2 == 1

def is_enclosed(matrix: Matrix, loop: set[tuple[int,int]], row: int, col: int) -> bool:
    #if position is part of the loop, it's instant no
    if (row, col) in loop:
        return False

    #let's explore in all directions, the tile is enclosed only if we find a loop in all directions
    # is_loop_up = is_there_odd_loop_in_direction(matrix, loop, {*valid_connections["left"], *valid_connections["right"]}, (row, col), lambda x: (x[0]-1, x[1]))
    # is_loop_down = is_there_odd_loop_in_direction(matrix, loop, {*valid_connections["left"], *valid_connections["right"]}, (row, col), lambda x: (x[0]+1, x[1]))
    is_loop_left = is_there_odd_loop_in_direction(matrix, loop, {*valid_connections["up"], *valid_connections["down"]}, (row, col), lambda x: (x[0], x[1]-1))
    # is_loop_right = is_there_odd_loop_in_direction(matrix, loop, {*valid_connections["up"], *valid_connections["down"]}, (row, col), lambda x: (x[0], x[1]+1))

    return is_loop_left

def print_loop(matrix: Matrix, loop_to_order: dict[tuple[int,int], int]) -> None:
    for row in range(matrix.row_count):
        line = []
        for col in range(matrix.col_count):
            add = matrix.get_item(row, col) if (row,col) not in loop_to_order else str(loop_to_order[(row, col)])
            line.append(add.ljust(5))
            
        print(" ".join(line))
        
#we just need whether it's horizontal, vertical or both
def get_s(matrix: Matrix, first: str, second: str) -> str:
    print(first)
    print(second)
    horizontal = False
    vertical = False
    if (first in valid_connections["up"] or second in valid_connections["down"]) or (second in valid_connections["up"] or first in valid_connections["down"]):
        vertical = True
    if (first in valid_connections["left"] or second in valid_connections["right"]) or (second in valid_connections["left"] or first in valid_connections["right"]):
        horizontal = True

    if horizontal and vertical:
        #example, we only need something which is bidirectional
        return "L"
    if horizontal:
        return "-"
    if vertical:
        return "|"

def solution(input: str) -> tuple[any, any]:
    matrix = Matrix(input)
    start = find_start(matrix)
    print(start)
    loop_to_order = {start : 0}
    loop = { start }
    pipes = [get_connecting_pipe(matrix, start, loop), get_connecting_pipe(matrix, start, loop)]
    first_pipes = [start, pipes[0]]
    second_pipes = [pipes[1]]
    while any(pipes):
        # print(matrix.get_item(pipes[0][0], pipes[0][1]))
        for i in range(len(pipes)):
            pipes[i] = get_connecting_pipe(matrix, pipes[i], loop)
        if pipes[0]:
            first_pipes.append(pipes[0])
        if pipes[1]:
            second_pipes.append(pipes[1])
    
    second_pipes.reverse()
    first_pipes.extend(second_pipes)
    loop_to_order = {}
    for i, elem in enumerate(first_pipes):
        loop_to_order[elem] = i

    print_loop(matrix, loop_to_order)
    # s = get_s(matrix, matrix.get_item(first_pipes[1][0], first_pipes[1][1]), matrix.get_item(first_pipes[-1][0], first_pipes[-1][1]))
    matrix.matrix[start[0]][start[1]] = "|"

    enclosed_tiles = 0
    #we have the loop now, let's check the area
    #if performance would be bad, we can limit our search to the rectange of the outer loop then probably
    for row in range(matrix.row_count):
        for col in range(matrix.col_count):
            if is_enclosed(matrix, loop, row, col):
                enclosed_tiles += 1
                
    print(enclosed_tiles)
    return (None, enclosed_tiles)

# input = """...........
# .S-------7.
# .|F-----7|.
# .||.....||.
# .||.....||.
# .|L-7.F-J|.
# .|..|.|..|.
# .L--J.L--J.
# ..........."""
# input = """.F----7F7F7F7F-7....
# .|F--7||||||||FJ....
# .||.FJ||||||||L7....
# FJL7L7LJLJ||LJ.L-7..
# L--J.L7...LJS7F-7L7.
# ....F-J..F7FJ|L7L7L7
# ....L7.F7||L7|.L7L7|
# .....|FJLJ|FJ|F7|.LJ
# ....FJL-7.||.||||...
# ....L---J.LJ.LJLJ..."""
# input = """FF7FSF7F7F7F7F7F---7
# L|LJ||||||||||||F--J
# FL-7LJLJ||||||LJL-77
# F--JF--7||LJLJ7F7FJ-
# L---JF-JLJ.||-FJLJJ7
# |F|F-JF---7F7-L7L|7|
# |FFJF7L7F-JF7|JL---7
# 7-L-JL7||F7|L7F-7F7|
# L.L7LFJ|||||FJL7||LJ
# L7JLJL-JLJLJL--JLJ.L
# """
# print(solution(input))
puzzle = Puzzle(2023, 10)
test_and_submit(puzzle, solution, False)