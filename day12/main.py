from aocd.models import Puzzle

from core import test_and_submit
from util import get_lines

def can_fit(window: str, to_place: int, record: str, before_index: int, after_index: int) -> bool:
    if before_index >= 0 and record[before_index] == "#":
        print("first return false")
        return False
    if after_index < len(record) and record[after_index] == "#":
        print("second return false")
        return False
    
    # print(window)
    return len(window) >= to_place and "." not in window

def get_combinations(record: str, groups: list[int], required_static_springs: int, found_windows: list[str]) -> int:
    # print(record, groups)
    if len(groups) == 0:
        static_springs_found = sum([window.count("#") for window in found_windows])
        if static_springs_found != required_static_springs:
            return 0
        # print("Found a solution")
        # print(found_windows)
        return 1

    to_place = groups[0]
    combinations = 0
    for i in range(1, len(record)):
        window = record[i:i+to_place]
        # print(f"checking: {i, i+to_place-1, window}")
        if can_fit(window, to_place, record, i-1, i+to_place):
            # print(f"found a window: {i, i+to_place-1, window}")
            combinations += get_combinations(record[i+to_place:], groups[1:], required_static_springs, found_windows + [window])
    
    return combinations

def solution(input: str) -> tuple[any, any]:
    lines = get_lines(input)
    sum = 0
    for line in lines:
        record, groups = line.split(" ")
        groups = [int(x) for x in groups.split(",")]
        #we pad the beginning of the string with a dot to ease processing
        required_static_springs = record.count("#")
        line_result = get_combinations(f".{record}", groups, required_static_springs, [])
        # print(line_result)
        sum += line_result
    return (sum, None)

puzzle = Puzzle(2023, 12)
test_and_submit(puzzle, solution, False)