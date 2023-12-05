from aocd.models import Puzzle

from core import test_and_submit
from util import get_blocks, get_range_overlap

class SeedRange:
    def __init__(self, start: int, range_of: int) -> None:
        self.ranges = [(start, start + range_of - 1)]
        self.target_ranges = []

    def change_target_if_required(self, source_start: int, destination_start: int, range_of: int) -> None:
        new_ranges = []
        for i in range(len(self.ranges)):
            range_overlap = get_range_overlap(self.ranges[i], (source_start, source_start + range_of - 1))
            if range_overlap is not None:
                # print(f"Rule: {destination_start} {source_start} {range_of}")
                if self.ranges[i][0] < range_overlap[0]:
                    new_ranges.append((self.ranges[i][0], range_overlap[0]-1))
                destination_beginning = destination_start + (range_overlap[0] - source_start)
                destination = (destination_beginning, destination_beginning + (range_overlap[1] - range_overlap[0]))
                # print(f"{range_overlap} => {destination}")
                self.target_ranges.append(destination)
                if self.ranges[i][1] > range_overlap[1]:
                    new_ranges.append((range_overlap[1]+1, self.ranges[i][1]))
            else:
                new_ranges.append(self.ranges[i])
        self.ranges = new_ranges.copy()
            
    def finish_block(self) -> None:
        self.ranges.extend(self.target_ranges)
        self.target_ranges = []
        
    def get_min(self) -> int:
        return min([r[0] for r in self.ranges])
        

def solution(input: str) -> tuple[any, any]:
    blocks = get_blocks(input)
    target_ranges_all = [int(number) for number in blocks[0].strip().split(":")[1].strip().split(" ")]
    seed_ranges = []
    for i in range(0, len(target_ranges_all), 2):
        seed_ranges.append(SeedRange(target_ranges_all[i], target_ranges_all[i+1]))

    # seed_ranges = seed_ranges[:1]
    for block in blocks[1:]:
        # first line is the description
        for line in block.splitlines()[1:]:
            line_parts = line.split(" ")
            destination_start = int(line_parts[0])
            source_start = int(line_parts[1])
            range_of = int(line_parts[2])
            for seed_range in seed_ranges:
                seed_range.change_target_if_required(source_start, destination_start, range_of)
            
        for seed_range in seed_ranges:
            seed_range.finish_block()

    min_value = min([seed_range.get_min() for seed_range in seed_ranges])
    return (None, min_value)

puzzle = Puzzle(2023, 5)
test_and_submit(puzzle, solution, False)