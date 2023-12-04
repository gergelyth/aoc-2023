def get_lines(input: str) -> list[str]:
    return input.splitlines()

def get_2d_array(input: str) -> list[list[str]]:
    return [list(line) for line in get_lines(input)]

def get_item(matrix: list[list[str]], row: int, col: int) -> any:
    if row < 0 or row >= len(matrix) or col < 0 or col >= len(matrix[row]):
        return None

    return matrix[row][col]