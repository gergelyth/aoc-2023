from aocd.models import Puzzle
from core import test_and_submit
from util import *

def solution(input: str) -> tuple[any, any]:
    lines = get_lines(input)
    sum = 0
    for line in lines:
        first_digit = next(ch for ch in line if ch.isdigit())
        last_digit = next(ch for ch in reversed(line) if ch.isdigit())
        sum += int(f"{first_digit}{last_digit}")
    
    return (sum, None)

puzzle = Puzzle(2023, 1)
test_and_submit(puzzle, solution, False)