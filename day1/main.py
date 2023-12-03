from aocd.models import Puzzle
from core import test_and_submit
from util import get_lines

digit_words = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}

def get_included_digit_word(part: str) -> int | None:
    digits = [key for key, value in digit_words.items() if key in part]
    return digits[0] if len(digits) > 0 else None

def find_first_digit(line: str, is_reversed: bool) -> str:
    cumm_window = ""
    for ch in reversed(line) if is_reversed else line:
        if ch.isdigit():
            return ch

        cumm_window = f"{ch}{cumm_window}" if is_reversed else f"{cumm_window}{ch}"
        found_word = get_included_digit_word(cumm_window)
        if found_word:
            return digit_words[found_word]

def solution(input: str) -> tuple[any, any]:
    lines = get_lines(input)
    sum = 0
    for line in lines:
        first_digit = find_first_digit(line, False)
        last_digit = find_first_digit(line, True)
        sum += int(f"{first_digit}{last_digit}")

    return (sum, sum)

puzzle = Puzzle(2023, 1)
test_and_submit(puzzle, solution, False)