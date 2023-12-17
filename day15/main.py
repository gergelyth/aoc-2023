from aocd.models import Puzzle
from collections import OrderedDict

from core import test_and_submit

def hash(label: str) -> int:
    current = 0
    for ch in label:
        if ch == "\n":
            continue
        
        current = (current + ord(ch)) * 17 % 256
        
    return current

def solution(input: str) -> tuple[any, any]:
    operations = input.split(",")
    boxes = {i: OrderedDict() for i in range(256)}
    for operation in operations:
        if "=" in operation:
            label, focal_length = operation.split("=")
            box = boxes[hash(label)]
            box[label] = focal_length
        else:
            label = operation.split("-")[0]
            box = boxes[hash(label)]
            if label in box:
                box.pop(label)
            
    focus_power = 0
    for box_id, box in boxes.items():
        for lens_order, (label, focal_length) in enumerate(box.items()):
            focus_power += (1+box_id) * (lens_order+1) * int(focal_length)

    return (None, focus_power)

puzzle = Puzzle(2023, 15)
test_and_submit(puzzle, solution, False)