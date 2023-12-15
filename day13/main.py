from aocd.models import Puzzle
from math import floor, ceil

from core import test_and_submit
from util import get_lines, get_columns

def has_one_smudge(moving: str, static: str) -> bool:
    smudge_fixed = False
    for c1, c2 in zip(moving, static):
        if c1 != c2:
            if smudge_fixed:
                return False
            smudge_fixed = True
    return smudge_fixed

def get_start_of_reflection(elements: list[str]) -> int | None:
    #we'll only try to fix smudges with the moving line, because the reversed run will do the opposite
    #this array is now (potential_start, smudge_fixed)
    potential_starts = []
    for i in range(len(elements)):
        for j, potential_start in enumerate(potential_starts):
            #we compare the current element to the appropriate one from the end to see if it's still a candidate
            corresponding_index = len(elements)-1-(i-potential_start[0])
            if elements[i] != elements[corresponding_index]:
                if potential_start[1]:
                    #one smudge was already fixed
                    potential_starts.remove(potential_start)
                else:
                    if has_one_smudge(elements[i], elements[corresponding_index]):
                        #this is the first smudge, still allowing it
                        potential_starts[j] = (potential_start[0], True)
                        if corresponding_index == i+1:
                            return potential_start[0]
                    else:
                        #we have multiple smudges which we can't fix
                        potential_starts.remove(potential_start)
            elif corresponding_index == i+1 and potential_start[1]:
                return potential_start[0]
            
        if elements[i] == elements[-1]:
            potential_starts.append((i, False))
        elif has_one_smudge(elements[i], elements[-1]):
            potential_starts.append((i, True))

        if i == len(elements)-2:
            return i if has_one_smudge(elements[i], elements[-1]) else None
            
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
        
        print(pattern)
        raise Exception("No divider found")

    return (None, summary)

puzzle = Puzzle(2023, 13)
test_and_submit(puzzle, solution, False)