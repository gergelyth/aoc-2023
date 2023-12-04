from aocd.models import Puzzle

from core import test_and_submit
from util import get_2d_array, get_item


class EngineNumber:
    def __init__(self) -> None:
        self.number = 0

    def found_digit(self, digit: int, row: int, col: int) -> None:
        if self.number == 0:
            self.starting_coords = (row, col)
        self.number *= 10
        self.number += digit

    def finish_and_get_if_matters(
        self, matrix: list[list[str]], row: int, col: int
    ) -> int:
        self.end_coords = (row, col)
        return self.number if self.__does_number_matter(matrix) else 0

    def __does_number_matter(self, matrix: list[list[str]]) -> bool:
        # We do a +2 for the end coords, because we check one position to the right (+1) and range is non-inclusive so +1 as well
        for row in range(self.starting_coords[0] - 1, self.end_coords[0] + 2):
            # Same reason for +2 as above
            for col in range(self.starting_coords[1] - 1, self.end_coords[1] + 2):
                item = get_item(matrix, row, col)
                if item and item != "." and not item.isdigit():
                    # This means a symbol for us
                    return True

        return False


def solution(input: str) -> tuple[any, any]:
    matrix = get_2d_array(input)
    number_sum = 0

    current_number = None

    for row in range(len(matrix)):
        for col in range(len(matrix[row])):
            if matrix[row][col].isdigit():
                current_number = current_number if current_number else EngineNumber()
                current_number.found_digit(int(matrix[row][col]), row, col)
            else:
                if current_number:
                    number_sum += current_number.finish_and_get_if_matters(matrix, row, col-1)
                    current_number = None
        if current_number:
            number_sum += current_number.finish_and_get_if_matters(matrix, row, col)
            current_number = None

    return (number_sum, None)


puzzle = Puzzle(2023, 3)
test_and_submit(puzzle, solution, False)