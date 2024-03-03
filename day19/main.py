from aocd.models import Puzzle
import re
from typing import Callable

from core import test_and_submit
from util import get_lines

class Part:
    def __init__(self, line: str) -> None:
        line_match = re.match(r"{x=(.*),m=(.*),a=(.*),s=(.*)}", line)
        self.x = int(line_match.group(1))
        self.m = int(line_match.group(2))
        self.a = int(line_match.group(3))
        self.s = int(line_match.group(4))
        
    def sum(self) -> int:
        return self.x + self.m + self.a + self.s
        
class Workflow:
    def __init__(self, line: str) -> None:
        line_match = re.match(r"(.*){(.*)}", line)
        self.name = line_match.group(1)
        
        rules_str = line_match.group(2).split(",")
        self.rules = [self.__parse_rule(rule_str) for rule_str in rules_str]
        
    def run(self, part: Part) -> str:
        for rule in self.rules:
            action = rule(part)
            if action:
                return action
            
        raise Exception("The workflow didn't determine a definite action")
        
    #If we return None, we just pass because the condition wasn't fulfilled
    def __parse_rule(self, rule_str: str) -> Callable[[Part], str | None]:
        rule_match = re.match(r"(.*)(<|>)(.*):(.*)", rule_str)
        if rule_match:
            field = rule_match.group(1)
            operator = rule_match.group(2)
            threshold = int(rule_match.group(3))
            condition = self.__construct_condition(field, operator, threshold)
            
            action = rule_match.group(4)
            return lambda part: action if condition(part) else None
        else:
            action = rule_str
            return lambda _: action
            
    def __construct_condition(self, field: str, operator: str, threshold: int) -> Callable[[Part], bool]:
        if operator == "<":
            return lambda part: int(getattr(part, field)) < threshold
        else:
            return lambda part: int(getattr(part, field)) > threshold

def is_part_accepted(workflows: dict[str, Workflow], part: Part) -> bool:
    action = "in"
    while action != "A" and action != "R":
        workflow = workflows[action]
        action = workflow.run(part)
        
    return action == "A"
    
def solution(input: str) -> tuple[any, any]:
    lines = get_lines(input)
    workflows = {}
    parts = []
    
    is_workflow = True
    for line in lines:
        if line == "":
            is_workflow = False
            continue
        
        if is_workflow:
            workflow = Workflow(line)
            workflows[workflow.name] = workflow
        else:
            parts.append(Part(line))
    
    result = 0
    for part in parts:
        if is_part_accepted(workflows, part):
            result += part.sum()
        
    return (result, None)

puzzle = Puzzle(2023, 19)
test_and_submit(puzzle, solution, False)