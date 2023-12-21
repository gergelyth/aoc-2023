from aocd.models import Puzzle
import heapq

from core import test_and_submit
from util import Matrix, directions, add_tuples

def is_backward(*args: str) -> bool:
    args = sorted(args)
    return args == ["left", "right"] or args == ["down", "up"]

def dijkstra(matrix: Matrix, start: tuple[int,int], goal: tuple[int,int]):
    visited = set()
    # cost, position, direction, direction_count
    queue = [(0, start, "right", 1)]
    while len(queue) > 0:
        cost, current, direction, dir_count = heapq.heappop(queue)
        if (current, direction, dir_count) in visited:
            continue
        else:
            visited.add((current, direction, dir_count))

        new_position = add_tuples(current, directions[direction])
        new_position_cost = matrix.get_item_pos(new_position)
        #outside the bounds
        if new_position_cost is None:
            continue
        new_cost = cost + int(new_position_cost)

        # found the target with a good path
        if new_position == goal and dir_count <= 3:
            return new_cost
            
        for candidate_dir in directions:
            #we can't go back
            if is_backward(direction, candidate_dir):
                continue

            new_dir_count = dir_count + 1 if candidate_dir == direction else 1
            #we can't go 4 blocks straight
            if new_dir_count > 3:
                continue
            
            heapq.heappush(queue, (new_cost, new_position, candidate_dir, new_dir_count))

def solution(input: str) -> tuple[any, any]:
    matrix = Matrix(input)
    target = (matrix.row_count-1, matrix.col_count-1)
    result = dijkstra(matrix, (0, 0), target)
    return (result, None)

puzzle = Puzzle(2023, 17)
test_and_submit(puzzle, solution, False)