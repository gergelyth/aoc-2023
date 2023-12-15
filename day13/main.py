from aocd.models import Puzzle
from math import floor, ceil

from core import test_and_submit
from util import get_lines, get_columns

def get_start_of_reflection(elements: list[str]) -> int | None:
    potential_starts = []
    for i in range(len(elements)):
        for potential_start in potential_starts:
            #we compare the current element to the appropriate one from the end to see if it's still a candidate
            corresponding_index = len(elements)-1-(i-potential_start)
            if elements[i] != elements[corresponding_index]:
                potential_starts.remove(potential_start)
            elif corresponding_index == i+1:
                return potential_start
            
        if elements[i] == elements[-1]:
            if i == len(elements)-2:
                return i
            potential_starts.append(i)
            
    return None
            
def get_divider(elements: list[str]) -> tuple[int,int] | None:
    start_of_reflection = get_start_of_reflection(elements)
    if start_of_reflection:
        divider = start_of_reflection + (len(elements)-1 - start_of_reflection) / 2
        return floor(divider), ceil(divider)

    start_of_reflection = get_start_of_reflection(list(reversed(elements)))
    if not start_of_reflection:
        return None

    divider = (len(elements)-1 - start_of_reflection) / 2
    return floor(divider), ceil(divider)

def solution(input: str) -> tuple[any, any]:
    summary = 0
    for pattern in input.split("\n\n"):
        # print(pattern)
        lines = get_lines(pattern)
        horizontal_divider = get_divider(lines)
        if horizontal_divider:
            result = 100 * (horizontal_divider[0]+1)
            print(f"horizontal: {result}")
            summary += result
            continue

        columns = get_columns(lines)
        vertical_divider = get_divider(columns)
        if vertical_divider:
            result = vertical_divider[0]+1
            print(f"vertical: {result}")
            summary += result
            continue
        
        # print(pattern)
        # raise Exception("No divider found")

    return (summary, None)

puzzle = Puzzle(2023, 13)
test_and_submit(puzzle, solution, False)