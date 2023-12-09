from aocd.models import Puzzle
from itertools import pairwise

from core import test_and_submit
from util import get_lines

def process_line(line: str) -> int:
    sequence = [int(x) for x in line.split(" ")]
    last_values = [sequence[-1]]
    
    #while there is a differing value
    while sequence.count(sequence[0]) != len(sequence):
        sequence = [y - x for (x, y) in pairwise(sequence)]
        last_values.append(sequence[-1])
        
    #we only need to add the last values in the lines together as the extrapolated value is just this
    return sum(last_values)

def solution(input: str) -> tuple[any, any]:
    lines = get_lines(input)
    result_sum = 0
    for line in lines:
        result_sum += process_line(line)
            
    return (result_sum, None)

puzzle = Puzzle(2023, 9)
test_and_submit(puzzle, solution, False)