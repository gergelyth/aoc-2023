from aocd.models import Puzzle
from typing import Callable
from glob import glob
import shutil

def invalidate_cache():
    shutil.rmtree(glob("/home/vscode/.config/aocd/*gergelyth*")[0])
    shutil.rmtree("/home/vscode/.config/aocd/prose")

# As arguments, we take the puzzle and the algorithm which computes answer A and answer B.
def test_and_submit(puzzle: Puzzle, algorithm: Callable[[str], tuple[any, any]], dry_run: bool = True):
    examples = puzzle.examples[len(puzzle.examples)//2:] if puzzle.answered_a else puzzle.examples
    for example in examples:
        test_result = algorithm(example.input_data)
        if not puzzle.answered_a and example.answer_a and str(test_result[0]) != str(example.answer_a):
            raise AssertionError(f"Test A failed. Expected result: {example.answer_a}, got: {test_result[0]}")
        if example.answer_b and str(test_result[1]) != str(example.answer_b):
            raise AssertionError(f"Test B failed. Expected result: {example.answer_b}, got: {test_result[1]}")
        
    print("All primary tests passed.")
    if dry_run:
        return
    
    live_result = algorithm(puzzle.input_data)
    
    if not puzzle.answered_a:
        puzzle.answer_a = live_result[0]
        if puzzle.answered_a:
            invalidate_cache()
        return
        
    if not puzzle.answered_b:
        puzzle.answer_b = live_result[1]
        return