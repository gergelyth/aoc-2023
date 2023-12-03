from aocd.models import Puzzle
import re
from math import prod

from core import test_and_submit
from util import get_lines

limit = {"red": 12, "green": 13, "blue": 14}

def convert_game_to_ctc(game_desc: str) -> tuple[int, str]:
    for iteration in game_desc.split(";"):
        for count_to_color in iteration.strip().split(","):
            ctc_match = re.match(r"(\d+) (\w+)", count_to_color.strip())
            count = int(ctc_match.group(1))
            color = ctc_match.group(2)
            
            yield count, color

def is_game_possible(game_desc: str) -> bool:
    for count, color in convert_game_to_ctc(game_desc):
        if count > limit[color]:
            return False

    return True

def get_power_of_fewest_cubes(game_desc: str) -> int:
    min_values = {"red": 0, "green": 0, "blue": 0}
    for count, color in convert_game_to_ctc(game_desc):
        if min_values[color] < count:
            min_values[color] = count
            
    return prod(min_values.values())

def solution(input: str) -> tuple[any, any]:
    lines = get_lines(input)
    possible_game_id_sum = 0
    min_values_sum = 0

    for line in lines:
        game_match = re.match(r"Game (\d+):(.*)", line)
        game_id = int(game_match.group(1))
        game_desc = game_match.group(2)

        if is_game_possible(game_desc):
            possible_game_id_sum += game_id
            
        min_values_sum += get_power_of_fewest_cubes(game_desc)

    return (possible_game_id_sum, min_values_sum)

puzzle = Puzzle(2023, 2)
test_and_submit(puzzle, solution, False)