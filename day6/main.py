from aocd.models import Puzzle

from core import test_and_submit
from util import get_lines

class Race:
    def __init__(self, time: int, distance: int) -> None:
        self.time = time
        self.max_distance = distance
        
    def get_possible_button_times(self) -> int:
        possible_ways = 0
        for hold_button_time in range(self.time):
            distance_traveled = hold_button_time * (self.time - hold_button_time)
            if distance_traveled > self.max_distance:
                possible_ways += 1
                
        return possible_ways
        
def parse_race(lines: list[str]) -> Race:
    times = list(filter(None, lines[0].split(" "))) 
    distances = list(filter(None, lines[1].split(" "))) 
    time = "".join(times[1:]).strip()
    distance = "".join(distances[1:]).strip()
    return Race(int(time), int(distance))

def solution(input: str) -> tuple[any, any]:
    lines = get_lines(input)
    race = parse_race(lines)
    possible_ways = race.get_possible_button_times()
    return (None, possible_ways)

puzzle = Puzzle(2023, 6)
test_and_submit(puzzle, solution, False)