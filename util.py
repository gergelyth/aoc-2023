def get_lines(input: str) -> list[str]:
    return input.splitlines()

def get_2d_array(input: str) -> list[list[str]]:
    return [list(line) for line in get_lines(input)]

def get_item(matrix: list[list[str]], row: int, col: int) -> any:
    if row < 0 or row >= len(matrix) or col < 0 or col >= len(matrix[row]):
        return None

    return matrix[row][col]

def get_blocks(input: str) -> list[list[str]]:
    return input.split("\n\n")

def get_range_overlap(x: tuple[int,int], y: tuple[int,int]) -> tuple[int,int] | None:
    overlap = max(x[0], y[0]), min(x[1], y[1])
    return overlap if overlap[0] <= overlap[1] else None