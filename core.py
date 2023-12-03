from aocd.models import Puzzle
from typing import Callable

# As arguments, we take the puzzle and the algorithm which computes answer A and answer B.
def test_and_submit(puzzle: Puzzle, algorithm: Callable[[str], tuple[any, any]], dry_run: bool = True):
    for example in puzzle.examples:
        test_result = algorithm(example.input_data)
        if str(test_result[0]) != str(example.answer_a):
            raise AssertionError(f"Test A failed. Expected result: {example.answer_a}, got: {test_result[0]}")
        if str(test_result[1]) != str(example.answer_b):
            raise AssertionError(f"Test B failed. Expected result: {example.answer_b}, got: {test_result[1]}")
        
    print("All primary tests passed.")
    if dry_run:
        return
    
    live_result = algorithm(puzzle.input_data)
    if not puzzle.answered_a:
        puzzle.answer_a = live_result[0]
        return
    if not puzzle.answered_b:
        puzzle.answer_b = live_result[1]
        return