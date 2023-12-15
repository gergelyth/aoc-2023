from aocd.models import Puzzle

from core import test_and_submit

def solution(input: str) -> tuple[any, any]:
    sum = 0
    current = 0
    for ch in input:
        if ch == "\n":
            continue
        if ch == ",":
            sum += current
            current = 0
            continue
        
        current = (current + ord(ch)) * 17 % 256
            
    sum += current
    return (sum, None)

puzzle = Puzzle(2023, 15)
test_and_submit(puzzle, solution, False)