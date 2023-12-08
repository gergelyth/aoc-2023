from aocd.models import Puzzle
import re

from core import test_and_submit
from util import get_lines

class Path:
    def __init__(self, short_map: dict[str, tuple[str,set[int]]], starting_node: str) -> None:
        self.short_map = short_map
        self.current_node = starting_node
        
    def get_ending_steps(self) -> set[int]:
        ending_steps = self.short_map[self.current_node][1]
        self.current_node = self.short_map[self.current_node][0]
        return ending_steps
    
def get_short_map(desert_map: dict[str, tuple[str,str]], instructions: str) -> dict[str, tuple[str, set[int]]]:
    short_map = {}
    for node in desert_map:
        current_node = node
        steps_to_end = set()
        for i, instruction in enumerate(instructions):
            direction = 0 if instruction == "L" else 1
            current_node = desert_map[current_node][direction]
            if current_node[-1] == "Z":
                steps_to_end.add(i+1)
        
        #ending node and finishing steps
        short_map[node] = (current_node, steps_to_end)

    return short_map

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
            
        desert_map[from_node] = (left, right)
        
    #we increase the length of the instruction to increase performance - this finishes in 2 minutes
    heuristic_instruction = instructions * 5000
    short_map = get_short_map(desert_map, heuristic_instruction)
    paths = [Path(short_map, starting_node) for starting_node in starting_points]

    steps = 0
    finish_timestep = None
    while not finish_timestep:
        ending_step_sets = [path.get_ending_steps() for path in paths]
        intersection = set.intersection(*ending_step_sets)
        #we take min so in case we multiple finishing timesteps, we take the first one
        finish_timestep = min(intersection, default=None)
        if finish_timestep:
            steps += finish_timestep
            break
        steps += len(heuristic_instruction)
        
    return (None, steps)

puzzle = Puzzle(2023, 8)
test_and_submit(puzzle, solution, False)