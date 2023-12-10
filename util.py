from collections import Counter

class Matrix:
    def __init__(self, input: str) -> None:
        self.matrix = get_2d_array(input)
        self.row_count = len(self.matrix)
        self.col_count = len(self.matrix[0])

    def get_item(self, row: int, col: int) -> any:
        if row < 0 or row >= self.row_count or col < 0 or col >= self.col_count:
            return None

        return self.matrix[row][col]
    
def get_lines(input: str) -> list[str]:
    return input.splitlines()

def get_2d_array(input: str) -> list[list[str]]:
    return [list(line) for line in get_lines(input)]

def get_blocks(input: str) -> list[list[str]]:
    return input.split("\n\n")

def get_range_overlap(x: tuple[int,int], y: tuple[int,int]) -> tuple[int,int] | None:
    overlap = max(x[0], y[0]), min(x[1], y[1])
    return overlap if overlap[0] <= overlap[1] else None

def first_list_contains_second(first: list[int], second: list[int]) -> bool:
    return not (Counter(second) - Counter(first))