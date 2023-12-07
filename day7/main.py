from aocd.models import Puzzle

from core import test_and_submit
from functools import cmp_to_key
from util import get_lines, first_list_contains_second
from collections import Counter

class Hand:
    def __init__(self, line: str) -> None:
        lineParts = line.split(" ")
        self.hand = lineParts[0]
        self.bid = int(lineParts[1])
        self.type = self.__determine_type(self.hand)
        
    def __determine_type(self, hand: str) -> int:
        card_count = Counter(hand)
        #we have 7 types, 7 is the highest (five of a kind), no time for an enum
        # print(card_count)
        jokers = card_count.pop("J", 0)
        #if we have 5 jokers, we default to 5 aces
        max_card = max(card_count, key=card_count.get, default="A")
        card_count[max_card] = card_count[max_card] + jokers
        counts = list(card_count.values())

        hand_type_order = [[5], [4], [3,2], [3], [2,2], [2], [1]]
        #find index of the combination which is included in our hand
        index = next(i for i, hand_type in enumerate(hand_type_order) if first_list_contains_second(counts, hand_type))
        #we want to give higher weight to earlier elements
        return len(hand_type_order) - index
        
def compare_cards(first: str, second: str) -> int:
    order = ["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J"]
    # this is the other way because we want ascending order
    return order.index(second) - order.index(first)    

def compare_hands(first: Hand, second: Hand) -> int:
    #returns a negative number if first is a lower hand
    if first.type != second.type:
        return first.type - second.type
    
    for i in range(5):
        card_comparison = compare_cards(first.hand[i], second.hand[i])
        if card_comparison != 0:
            return card_comparison
        
    return 0

def solution(input: str) -> tuple[any, any]:
    lines = get_lines(input)
    hands = [Hand(line) for line in lines]

    sorted_hands = sorted(hands, key=cmp_to_key(compare_hands))
    sum_result = 0
    for rank, hand in enumerate(sorted_hands):
        sum_result += (rank+1) * hand.bid

    return (None, sum_result)

puzzle = Puzzle(2023, 7)
test_and_submit(puzzle, solution, False)