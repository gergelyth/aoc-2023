from aocd.models import Puzzle
import re

from core import test_and_submit
from util import get_lines

limit = {"red": 12, "green": 13, "blue": 14}

def is_game_possible(game_desc: str) -> bool:
    for iteration in game_desc.split(";"):
        for count_to_color in iteration.strip().split(","):
            ctc_match = re.match(r"(\d+) (\w+)", count_to_color.strip())
            count = int(ctc_match.group(1))
            color = ctc_match.group(2)
            
            if count > limit[color]:
                return False

    return True

def solution(input: str) -> tuple[any, any]:
    lines = get_lines(input)
    game_id_sum = 0
    for line in lines:
        game_match = re.match(r"Game (\d+):(.*)", line)
        game_id = int(game_match.group(1))
        game_desc = game_match.group(2)

        if is_game_possible(game_desc):
            game_id_sum += game_id

    return (game_id_sum, None)

puzzle = Puzzle(2023, 2)
test_and_submit(puzzle, solution, False)