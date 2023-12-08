from aocd.models import Puzzle
import re

from core import test_and_submit
from util import get_lines

class Path:
    def __init__(self, desert_map: dict[str, tuple[str,str]], starting_node: str) -> None:
        self.desert_map = desert_map
        self.current_node = starting_node
        
    #return did finish flag
    def iterate(self, direction: int) -> bool:
        self.current_node = self.desert_map[self.current_node][direction]
        return self.current_node[-1] == "Z"

def solution(input: str) -> tuple[any, any]:
    lines = get_lines(input)
    instructions = lines[0]

    desert_map = {}
    starting_points = []
    for line in lines[2:]:
        line_parts = line.split("=")
        direction_match = re.match(r"\s*\((\w+),\s*(\w+)\)\s*", line_parts[1])
        left, right = direction_match.group(1).strip(), direction_match.group(2).strip()

        from_node = line_parts[0].strip()
        if from_node[-1] == "A":
            starting_points.append(from_node)
            
        desert_map[from_node] =  (left, right)
        
    paths = [Path(desert_map, starting_node) for starting_node in starting_points]
    steps = 0
    all_finished = False
    while (not all_finished):
        for instruction in instructions:
            direction = 0 if instruction == "L" else 1
            all_finished = True

            for path in paths:
                all_finished &= path.iterate(direction)

            steps += 1
            if all_finished:
                break
            
        print(steps)
    
    return (None, steps)

puzzle = Puzzle(2023, 8)
test_and_submit(puzzle, solution, False)