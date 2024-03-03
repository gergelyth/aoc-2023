from aocd.models import Puzzle
from collections import defaultdict

from core import test_and_submit
from util import get_lines, add_tuples, directions

mapping = {"R": "right", "D": "down", "L": "left", "U": "up"}
mapping_keys = list(mapping.keys())

class PlanStep:
    def __init__(self, line: str) -> None:
        direction, count, rgb_raw = line.split(" ")
        self.rgb = rgb_raw[1:-1]

        self.direction = mapping[mapping_keys[int(self.rgb[-1])]]
        self.count = int(self.rgb[1:-1], 16)

        self.is_horizontal = self.direction == "left" or self.direction == "right"
        #This will be true for horizontal movements which create a dead-end, i.e. if the previous movement is up and the next is down or vice versa
        #Those don't count as "opening" walls
        self.is_hook = False
        
    def __str__(self) -> str:
        return str((self.direction, self.count))
        
def print_inside(edge: set[str], min_row: int, max_row: int, min_col: int, max_col: int, inside: set[tuple[int,int]]):
    rows = []
    for row in range(min_row, max_row):
        rows.append("".join(["#" if (row,col) in edge else "*" if (row,col) in inside else "." for col in range(min_col, max_col)]))
    res = "\n".join(rows)
    file = open("inside.txt", "w")
    file.write(res)
    file.close()

def solution(input: str) -> tuple[any, any]:
    lines = get_lines(input)
    steps = []
    for line in lines:
        steps.append(PlanStep(line))
        
    min_row = 0
    max_row = 0
    
    #1. divide steps into horizontal and vertical
    #2. horizontal rules will have is_hook decided
    #3. we have vertical rules sorted by col number
    #4. we go row by row
        #5. we create rules of interest - all horizontal rules for the row and all vertical rules which cross the row
        #6. sort these by col number - for vertical rules use col number, for horizontal rules use start number
        #7. we iterate these sorted rules 
                #- if vertical, we toggle inside/outside
                #- if horizontal, toggle inside/outside if not hook
    
    padded_steps = [steps[-1], *steps, steps[1]]
    current = (0,0)
    for prev, curr, next in zip(padded_steps, padded_steps[1:], padded_steps[2:]):
        curr.start = current
        current = add_tuples(current, tuple([x * curr.count for x in directions[curr.direction]]))
        curr.end = current
        min_row = min(min_row, current[0])
        max_row = max(max_row, current[0])

        if curr.is_horizontal:
            if prev.direction != next.direction:
                curr.is_hook = True
                
    #sort steps from left to right
    steps.sort(key=lambda step: min(step.start[1], step.end[1]))

    row_to_relevant_steps = defaultdict(list)
    for step in steps:
        if step.is_horizontal:
            row_to_relevant_steps[step.start[0]] += [step]
        else:
            for row in range(min(step.start[0], step.end[0])+1, max(step.start[0], step.end[0])):
                row_to_relevant_steps[row] += [step]
    
    print((min_row, max_row))
    
    result = 0
    for row in range(min_row, max_row+1):
        relevant_steps = row_to_relevant_steps[row]
        inside = False
        start = 0
        # for first_step, second_step in zip(relevant_steps, relevant_steps[1:]):
        for step in relevant_steps:
            if step.is_horizontal:
                step_min = min(step.start[1], step.end[1])
                step_max = max(step.start[1], step.end[1])
                if inside:
                    #-1 so we don't count the beginning of the edge
                    result += step_min - start - 1
                    
                #this is the edge itself
                result += step_max - step_min + 1
                start = step_max
                if not step.is_hook:
                    inside = not inside
                    
            else:
                if inside:
                    #-1 so we don't count the edge
                    result += step.start[1] - start - 1

                #this is the edge itself
                result += 1
                inside = not inside
                start = step.start[1]
                
    return (None, result)

puzzle = Puzzle(2023, 18)
test_and_submit(puzzle, solution, False)