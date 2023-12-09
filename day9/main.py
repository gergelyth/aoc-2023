from aocd.models import Puzzle
from itertools import pairwise
from functools import reduce

from core import test_and_submit
from util import get_lines

def process_line(line: str) -> int:
    sequence = [int(x) for x in line.split(" ")]
    first_values = [sequence[0]]
    
    #while there is a differing value
    while sequence.count(sequence[0]) != len(sequence):
        sequence = [y - x for (x, y) in pairwise(sequence)]
        first_values.append(sequence[0])
        
    #substract the first values from each other to extrapolate the first value
    return reduce(lambda x, y: y - x, reversed(first_values))

def solution(input: str) -> tuple[any, any]:
    lines = get_lines(input)
    result_sum = 0
    for line in lines:
        result_sum += process_line(line)
            
    return (None, result_sum)

puzzle = Puzzle(2023, 9)
test_and_submit(puzzle, solution, False)