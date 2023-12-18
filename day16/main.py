from aocd.models import Puzzle

from core import test_and_submit
from util import Matrix, directions, add_tuples

forward_slash = {
    "up": "right",
    "down": "left",
    "left": "down",
    "right": "up"
}

backslash = {
    "up": "left",
    "down": "right",
    "left": "up",
    "right": "down"
}

class Beam:
    def __init__(self, current_pos: tuple[int,int], direction: str) -> None:
        self.current_pos = current_pos
        self.direction = direction
        
    def is_finished(self, matrix: Matrix) -> bool:
        return matrix.get_item_pos(self.current_pos) is None
    
    #this is Beam | None
    def move(self, matrix: Matrix) -> any:
        new_beam = None
        if matrix.get_item_pos(self.current_pos) == "/":
            self.direction = forward_slash[self.direction]
        if matrix.get_item_pos(self.current_pos) == "\\":
            self.direction = backslash[self.direction]
        if matrix.get_item_pos(self.current_pos) == "|":
            if self.direction == "left" or self.direction == "right":
                self.direction = "up"
                new_beam = Beam(self.current_pos, "down")
        if matrix.get_item_pos(self.current_pos) == "-":
            if self.direction == "up" or self.direction == "down":
                self.direction = "left"
                new_beam = Beam(self.current_pos, "right")
                
        self.current_pos = add_tuples(self.current_pos, directions[self.direction])
        return new_beam

def solution(input: str) -> tuple[any, any]:
    matrix = Matrix(input)
    beams = [Beam((0, 0), "right")]
    visited = {}
    while len(beams) > 0:
        new_beams = []
        for beam in beams:
            if beam.current_pos in visited:
                if beam.direction in visited[beam.current_pos]:
                    beams.remove(beam)
                else:
                    visited[beam.current_pos].append(beam.direction)
            else:
                visited[beam.current_pos] = [beam.direction]

            new_beams.append(beam.move(matrix))
            if beam.is_finished(matrix) and beam in beams:
                beams.remove(beam)
                
        beams.extend(list(filter(None, new_beams)))
        
    return (len(visited), None)

puzzle = Puzzle(2023, 16)
test_and_submit(puzzle, solution, False)