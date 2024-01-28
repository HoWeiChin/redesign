from collections import defaultdict
from typing import Callable

rules_factory: dict[str, Callable[[int, int], int]] = defaultdict(lambda : "Rule is absent")

def BirthRule(cell, live_neighbors):
    if cell == 0 and live_neighbors == 3:
        return 1
    return None

def LonelyDeathRule(cell, live_neighbors):
    if cell == 1 and live_neighbors < 2:
        return 0
    return None

def StayAliveRule(cell, live_neighbors):
    if cell == 1 and 2 <= live_neighbors <= 3:
        return 1
    return None

def OverPopulateRule(cell, live_neighbors):
    if cell == 1 and live_neighbors > 3:
        return 0
    return None

rules_factory["BirthRule"] = BirthRule
rules_factory["LonelyDeathRule"] = LonelyDeathRule
rules_factory["StayAliveRule"] = StayAliveRule
rules_factory["OverPopulateRule"] = OverPopulateRule



