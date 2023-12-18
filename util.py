from collections import Counter

directions = {
    "up": (-1, 0),
    "down": (1, 0),
    "left": (0, -1),
    "right": (0, 1)
}

class Matrix:
    def __init__(self, input: str) -> None:
        self.matrix = get_2d_array(input)
        self.row_count = len(self.matrix)
        self.col_count = len(self.matrix[0])

    def get_item_pos(self, position: tuple[int, int]) -> any:
        return self.get_item(position[0], position[1])

    def get_item(self, row: int, col: int) -> any:
        if row < 0 or row >= self.row_count or col < 0 or col >= self.col_count:
            return None

        return self.matrix[row][col]

    def set_item(self, row: int, col: int, item: any) -> None:
        if row < 0 or row >= self.row_count or col < 0 or col >= self.col_count:
            return
        self.matrix[row][col] = item
        
    def __str__(self) -> str:
        rows = []
        for row in range(self.row_count):
            rows.append("".join([self.matrix[row][col] for col in range(self.col_count)]))
        return ",".join(rows)

    def print(self) -> None:
        for row in range(self.row_count):
            print("".join([self.matrix[row][col] for col in range(self.col_count)]))
            
def get_lines(input: str) -> list[str]:
    return input.splitlines()

def get_columns(lines: list[str]) -> list[str]:
    columns = []
    for i in range(len(lines[0])):
        columns.append(str([line[i] for line in lines]))
    return columns

def get_2d_array(input: str) -> list[list[str]]:
    return [list(line) for line in get_lines(input)]

def get_blocks(input: str) -> list[list[str]]:
    return input.split("\n\n")

def get_range_overlap(x: tuple[int,int], y: tuple[int,int]) -> tuple[int,int] | None:
    overlap = max(x[0], y[0]), min(x[1], y[1])
    return overlap if overlap[0] <= overlap[1] else None

def first_list_contains_second(first: list[int], second: list[int]) -> bool:
    return not (Counter(second) - Counter(first))

def add_tuples(first: tuple, second: tuple) -> tuple:
    return tuple(map(lambda x, y: x + y, first, second))