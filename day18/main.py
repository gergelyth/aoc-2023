from aocd.models import Puzzle

from core import test_and_submit
from util import get_lines, add_tuples, directions

mapping = {"R": "right", "D": "down", "L": "left", "U": "up"}

class PlanStep:
    def __init__(self, line: str) -> None:
        direction, count, rgb_raw = line.split(" ")
        self.direction = mapping[direction]
        self.count = int(count)
        #This will be true for horizontal movements which create a dead-end, i.e. if the previous movement is up and the next is down or vice versa
        #Those don't count as "opening" walls
        self.is_hook = False
        self.rgb = rgb_raw[1:-1]
        
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
        
    padded_steps = [steps[-1], *steps, steps[1]]
    for prev, curr, next in zip(padded_steps, padded_steps[1:], padded_steps[2:]):
        if curr.direction == "left" or curr.direction == "right":
            if prev.direction != next.direction:
                curr.is_hook = True
        
    edge = {}

    current = (0,0)
    for step in steps:
        if step.direction == "left" or step.direction == "right":
            #This is needed so corners of the edge don't represent up/down movements, but will point to left/right
            edge[current] = step
        for _ in range(step.count):
            current = add_tuples(current, directions[step.direction])
            edge[current] = step
        
    #We do the same as above for left/right for when the loop is completed to cover the edge case
    edge[(0,0)] = steps[0]
            
    min_row = min(e[0] for e in edge.keys())
    max_row = max(e[0] for e in edge.keys())+1
    min_col = min(e[1] for e in edge.keys())
    max_col = max(e[1] for e in edge.keys())+1
    
    result_list = set()
    result = 0
    for row in range(min_row, max_row):
        counted_steps = set()
        inside = False
        for col in range(min_col, max_col):
            if (row,col) in edge:
                result += 1
                result_list.add((row, col))
                step = edge[(row, col)]
                if step not in counted_steps and not step.is_hook:
                    inside = not inside
                    counted_steps.add(step)
            else:
                if inside:
                    result_list.add((row, col))
                    result += 1
        
    print_inside(edge.keys(), min_row, max_row, min_col, max_col, result_list)
    return (result, None)

puzzle = Puzzle(2023, 18)
test_and_submit(puzzle, solution, False)