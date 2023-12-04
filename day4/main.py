from aocd.models import Puzzle
import re

from core import test_and_submit
from util import get_lines

def solution(input: str) -> tuple[any, any]:
    lines = get_lines(input)
    result_sum = 0
    for line in lines:
        match = re.match(r".*: (.*) \| (.*)", line)
        winning_numbers = set(match.group(1).strip().split(" "))
        owned_numbers = set(match.group(2).strip().split(" "))
        matching_numbers = list(filter(None, winning_numbers.intersection(owned_numbers)))
        result_sum += 2 ** (len(matching_numbers)-1) if len(matching_numbers) > 0 else 0

    return (result_sum, None)


puzzle = Puzzle(2023, 4)
test_and_submit(puzzle, solution, False)