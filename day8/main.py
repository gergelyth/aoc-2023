from aocd.models import Puzzle
import re

from core import test_and_submit
from util import get_lines

def solution(input: str) -> tuple[any, any]:
    lines = get_lines(input)
    instructions = lines[0]

    desert_map = {}
    for line in lines[2:]:
        line_parts = line.split("=")
        direction_match = re.match(r"\s*\((\w+),\s*(\w+)\)\s*", line_parts[1])
        left, right = direction_match.group(1).strip(), direction_match.group(2).strip()
        desert_map[line_parts[0].strip()] =  (left, right)
        
    steps = 0
    current_node = "AAA"
    while (current_node != "ZZZ"):
        for instruction in instructions:
            direction = 0 if instruction == "L" else 1
            current_node = desert_map[current_node][direction]
            steps += 1
            if current_node == "ZZZ":
                break
    
    return (steps, None)

puzzle = Puzzle(2023, 8)
test_and_submit(puzzle, solution, False)