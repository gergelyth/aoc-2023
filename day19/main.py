from __future__ import annotations
from aocd.models import Puzzle
import re
from typing import Callable

from core import test_and_submit
from util import get_lines

class PartRange:
    def __init__(self) -> None:
        self.x = (1, 4000)
        self.m = (1, 4000)
        self.a = (1, 4000)
        self.s = (1, 4000)
        
    def copy(self) -> PartRange:
        copy = PartRange()
        copy.x = self.x
        copy.m = self.m
        copy.a = self.a
        copy.s = self.s
        return copy
        
    def __str__(self) -> str:
        return f"x={self.x};m={self.m};a={self.a};s={self.s}"
        
class Workflow:
    def __init__(self, line: str) -> None:
        line_match = re.match(r"(.*){(.*)}", line)
        self.name = line_match.group(1)
        
        rules_str = line_match.group(2).split(",")
        self.rules = [self.__parse_rule(rule_str) for rule_str in rules_str]
        
    def run(self, part_range: PartRange):
        current = part_range
        for rule in self.rules:
            result_ranges_to_action = rule(current)
            for (range, action) in result_ranges_to_action:
                if range and action:
                    yield (range, action)
                    continue
                if range:
                    current = range
            
    def __parse_rule(self, rule_str: str) -> Callable[[PartRange], list[tuple[PartRange | None, str | None]]]:
        rule_match = re.match(r"(.*)(<|>)(.*):(.*)", rule_str)
        if rule_match:
            field = rule_match.group(1)
            operator = rule_match.group(2)
            threshold = int(rule_match.group(3))
            action = rule_match.group(4)
            split_function = self.__construct_split_function(field, operator, threshold, action)
            return split_function
        else:
            action = rule_str
            return lambda part_range: [(part_range, action)]
            
    def __construct_split_function(self, field: str, operator: str, threshold: int, action: str) -> Callable[[PartRange], list[tuple[PartRange | None, str | None]]]:
        def flood(part_range: PartRange) -> list[tuple[PartRange | None, str | None]]:
            #first will always be the interval passing the condition, the second is the one which doesn't
            condition_intervals = [(1, threshold-1), (threshold, 4000)] if operator == "<" else [(threshold+1, 4000), (1, threshold)]
            field_interval = getattr(part_range, field)
            intersects = [self.__get_intersect(condition_intervals[0], field_interval), self.__get_intersect(condition_intervals[1], field_interval)]
            
            cond_passing_copy = part_range.copy()
            setattr(cond_passing_copy, field, intersects[0])
            cond_passing_copy = cond_passing_copy if intersects[0] else None
            
            negative_case_copy = part_range.copy()
            setattr(negative_case_copy, field, intersects[1])
            negative_case_copy = negative_case_copy if intersects[1] else None
            
            result_parts = [(cond_passing_copy, action), (negative_case_copy, None)]
            return result_parts
        
        return flood
        
    def __get_intersect(self, x: tuple[int,int], y: tuple[int,int]) -> tuple[int,int] | None:
        intersect = (max(x[0], y[0]), min(x[1], y[1]))
        return intersect if intersect[0] < intersect[1] else None

def flood_workflows(workflows: dict[str, Workflow]):
    queue = [(PartRange(), "in")]
    while len(queue) > 0:
        part_range, action = queue.pop(0)
        if action == "R":
            continue
        if action == "A":
            yield part_range
            continue
            
        workflow = workflows[action]
        for result in workflow.run(part_range):
            queue.append(result)
    
def solution(input: str) -> tuple[any, any]:
    lines = get_lines(input)
    workflows = {}
    
    for line in lines:
        if line == "":
            break
        workflow = Workflow(line)
        workflows[workflow.name] = workflow
    
    final = 0
    for result in flood_workflows(workflows):
        # print(result)
        combinations = (result.x[1] - result.x[0] + 1) * (result.m[1] - result.m[0] + 1) * (result.a[1] - result.a[0] + 1) * (result.s[1] - result.s[0] + 1)
        final += combinations
        
    return (None, final)

puzzle = Puzzle(2023, 19)
test_and_submit(puzzle, solution, False)