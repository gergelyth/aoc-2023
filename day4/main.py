from aocd.models import Puzzle
import re

from core import test_and_submit
from util import get_lines

def solution(input: str) -> tuple[any, any]:
    lines = get_lines(input)
    points_total = 0
    copies_tracker = dict((i, 1) for i in range(0, len(lines)))
    for line_number, line in enumerate(lines):
        match = re.match(r".*: (.*) \| (.*)", line)
        winning_numbers = set(match.group(1).strip().split(" "))
        owned_numbers = set(match.group(2).strip().split(" "))
        matching_numbers = list(filter(None, winning_numbers.intersection(owned_numbers)))
        current_points = 2 ** (len(matching_numbers)-1) if len(matching_numbers) > 0 else 0
        points_total += current_points
        
        for i in range(line_number+1, line_number+len(matching_numbers)+1):
            copies_tracker[i] += copies_tracker[line_number]

    total_copies = sum(copies_tracker.values())
    return (points_total, total_copies)


puzzle = Puzzle(2023, 4)
test_and_submit(puzzle, solution, False)