from aocd.models import Puzzle
from math import prod

from core import test_and_submit
from util import get_lines

class Race:
    def __init__(self, time: int, distance: int) -> None:
        self.time = time
        self.max_distance = distance
        
    def get_possible_button_times(self) -> list[int]:
        results = []
        for hold_button_time in range(self.time):
            travel_time = self.time - hold_button_time
            distance_traveled = hold_button_time * travel_time
            if distance_traveled > self.max_distance:
                results.append(hold_button_time)
                
        return results
        
def parse_races(lines: list[str]) -> list[Race]:
    races = []
    times = list(filter(None, lines[0].split(" "))) 
    distances = list(filter(None, lines[1].split(" "))) 
    for i in range(1, len(times)):
        races.append(Race(int(times[i].strip()), int(distances[i].strip())))
    return races

def solution(input: str) -> tuple[any, any]:
    lines = get_lines(input)
    races = parse_races(lines)
    product = 1
    for race in races:
        result = len(race.get_possible_button_times())
        product *= result
    return (product, None)

puzzle = Puzzle(2023, 6)
test_and_submit(puzzle, solution, False)