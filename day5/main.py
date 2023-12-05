from aocd.models import Puzzle

from core import test_and_submit
from util import get_blocks

def change_target_if_required(targets: list[int], changed_in_block: list[bool], source_start: int, destination_start: int, range_of: int) -> None:
    for i in range(len(targets)):
        if not changed_in_block[i] and targets[i] >= source_start and targets[i] < source_start + range_of:
            targets[i] = destination_start + (targets[i] - source_start)
            changed_in_block[i] = True

def solution(input: str) -> tuple[any, any]:
    blocks = get_blocks(input)
    targets = [int(number) for number in blocks[0].strip().split(":")[1].strip().split(" ")]
    for block in blocks[1:]:
        changed_in_block = [False] * len(targets)
        # first line is the description
        for line in block.splitlines()[1:]:
            line_parts = line.split(" ")
            destination_start = int(line_parts[0])
            source_start = int(line_parts[1])
            range_of = int(line_parts[2])
            change_target_if_required(targets, changed_in_block, source_start, destination_start, range_of)
            
    min_value = min(targets)
    return (min_value, None)


puzzle = Puzzle(2023, 5)
test_and_submit(puzzle, solution, False)