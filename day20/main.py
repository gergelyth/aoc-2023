from __future__ import annotations
from typing import Literal
import re
from collections import defaultdict 
from aocd.models import Puzzle
import math
import numpy as np

from core import test_and_submit
from util import get_lines

class Pulse:
    def __init__(self, sender: Module, destination: Module, pulse_type: Literal["high", "low"]):
        self.sender = sender
        self.destination = destination
        self.type = pulse_type

class Module:
    def __init__(self, name: str) -> None:
        self.name = name
        self.should_record = False
        
    def set_connections(self, inputs: list[Module], destinations: list[Module]) -> None:
        self.inputs = inputs
        self.destinations = destinations
        
    def low_pulse(self, sender: Module) -> list[Pulse]:
        raise NotImplementedError("Override this")
    
    def high_pulse(self, sender: Module) -> list[Pulse]:
        raise NotImplementedError("Override this")
    
    def send_low_pulse(self) -> list[Pulse]:
        return [Pulse(self, destination, "low") for destination in self.destinations]

    def send_high_pulse(self) -> list[Pulse]:
        if self.should_record:
            self.func(self)
        return [Pulse(self, destination, "high") for destination in self.destinations]
    
    def record_high_pulse(self, func) -> None:
        self.func = func
        self.should_record = True
    
class FlipFlopModule(Module):
    def __init__(self, name: str) -> None:
        self.state = False
        super().__init__(name)
        
    def low_pulse(self, sender: Module) -> list[Pulse]:
        self.state = not self.state
        if self.state:
            return self.send_high_pulse()
        else:
            return self.send_low_pulse()
    
    def high_pulse(self, sender: Module) -> list[Pulse]:
        return []
    
class ConjunctionModule(Module):
    def set_connections(self, inputs: list[Module], destinations: list[Module]) -> None:
        super().set_connections(inputs, destinations)
        self.input_states = dict.fromkeys(self.inputs, "low")

    def low_pulse(self, sender: Module) -> list[Pulse]:
        self.input_states[sender] = "low"
        return self.send_high_pulse()
            
    def high_pulse(self, sender: Module) -> list[Pulse]:
        self.input_states[sender] = "high"
        if all(state == "high" for state in self.input_states.values()):
            return self.send_low_pulse()
        else:
            return self.send_high_pulse()
        
class BroadcastModule(Module):
    def low_pulse(self, sender: Module) -> list[Pulse]:
        return self.send_low_pulse()
    
    def high_pulse(self, sender: Module) -> list[Pulse]:
        return self.send_high_pulse()
    
class TestModule(Module):
    def low_pulse(self, sender: Module) -> list[Pulse]:
        return []
    
    def high_pulse(self, sender: Module) -> list[Pulse]:
        return []
    
def prepare_modules(lines: list[str]) -> dict[str, Module]:
    modules = {}
    inputs = defaultdict(list)
    destinations = defaultdict(list)
    
    for line in lines:
        line_match = re.match(r"(.*) -> (.*)", line)
        name_with_type = line_match.group(1)
        if name_with_type == "broadcaster":
            name = name_with_type
            module = BroadcastModule(name)
        elif name_with_type[0] == "%":
            name = name_with_type[1:]
            module = FlipFlopModule(name)
        elif name_with_type[0] == "&":
            name = name_with_type[1:]
            module = ConjunctionModule(name)
        else:
            name = name_with_type
            module = TestModule(name)
            
        destinations[name] = [dest.strip() for dest in line_match.group(2).split(",")]
        for dest in destinations[name]:
            inputs[dest] += [name]
            
        modules[name] = module
        
    for name, module in modules.items():
        module_dests = [modules[destination] if destination in modules else TestModule(destination) for destination in destinations[name]]
        module.set_connections([modules[input] for input in inputs[name]], module_dests)
        
    return modules

def solution(input: str) -> tuple[any, any]:
    lines = get_lines(input)
    modules = prepare_modules(lines)
    
    broadcaster = modules["broadcaster"]
    
    button_press = 0
    modules_of_interest = {}
    #Get the first state when the inputs of the module which reaches rx deliver a high pulse
    #Then just find the least common multiple of those - that will trigger the low pulse from "vr"
    for i in modules["vr"].inputs:
        modules_of_interest[i] = []
        
    def func(module):
        modules_of_interest[module].append(button_press)
        # print(f"{module.name} delivered a high pulse at {button_press}")
        
    for key, _ in modules_of_interest.items():
        key.record_high_pulse(func)

    while any(len(iteration) == 0 for iteration in modules_of_interest.values()):
        button_press += 1

        pulse_queue = []
        pulse_queue += broadcaster.low_pulse(None)
        
        while len(pulse_queue) > 0:
            pulse = pulse_queue.pop(0)
                
            result_pulses = pulse.destination.low_pulse(pulse.sender) if pulse.type == "low" else pulse.destination.high_pulse(pulse.sender)
            pulse_queue += result_pulses

    # result = math.lcm(modules_of_interest.values())
    result = np.lcm.reduce([*modules_of_interest.values()])[0]
    print(result)
    return (None, result)

puzzle = Puzzle(2023, 20)
test_and_submit(puzzle, solution, False)