# Generated using @xavdid's AoC Python Template: https://github.com/xavdid/advent-of-code-python-template

# puzzle prompt: https://adventofcode.com/2024/day/5

from collections import defaultdict
from functools import cmp_to_key

from ...base import StrSplitSolution, answer


def valid_update(update: list[int], rules: dict[int, set[int]]) -> bool:
    for i, elem in enumerate(update):
        if elem not in rules:
            continue
        for rule in rules[elem]:
            if rule in update and i < update.index(rule):
                return False
    return True


# Quite slow handmade method to reorder the update
def reorder_update(update: list[int], rules: dict[int, set[int]]) -> list[int]:
    for _ in update:
        for i, elem in enumerate(update):
            if elem not in rules:
                continue
            for rule in rules[elem]:
                if rule in update and i < (idx := update.index(rule)):
                    update.insert(idx + 1, elem)
                    update.pop(i)
                    break
    return update


class Solution(StrSplitSolution):
    _year = 2024
    _day = 5

    @answer(6505)
    def part_1(self) -> int:
        index = self.input.index("")
        rules_list, updates = (
            self.input[:index],
            [[int(x) for x in line.split(",")] for line in self.input[index + 1 :]],
        )

        rules = defaultdict(set)
        for rule in rules_list:
            l, r = map(int, rule.split("|"))
            rules[r].add(l)

        return sum(
            update[len(update) // 2]
            for update in updates
            if valid_update(update, rules)
        )

    @answer(6897)
    def part_2(self) -> int:
        index = self.input.index("")
        rules_list, updates = (
            self.input[:index],
            [[int(x) for x in line.split(",")] for line in self.input[index + 1 :]],
        )

        rules = defaultdict(set)
        for rule in rules_list:
            l, r = map(int, rule.split("|"))
            rules[r].add(l)

        def comparator(a, b):
            if b in rules[a]:
                return 1
            if a in rules[b]:
                return -1
            return 0

        return sum(
            sorted(update, key=cmp_to_key(comparator))[len(update) // 2]
            for update in updates
            if not valid_update(update, rules)
        )

    @answer((6505, 6897))
    def solve(self) -> tuple[int, int]:
        index = self.input.index("")
        rules_list, updates = (
            self.input[:index],
            [[int(x) for x in line.split(",")] for line in self.input[index + 1 :]],
        )

        rules = defaultdict(set)
        for rule in rules_list:
            l, r = map(int, rule.split("|"))
            rules[r].add(l)

        def comparator(a, b):
            if b in rules[a]:
                return 1
            if a in rules[b]:
                return -1
            return 0

        part1, part2 = 0, 0

        for update in updates:
            if valid_update(update, rules):
                part1 += update[len(update) // 2]
            else:
                part2 += sorted(update, key=cmp_to_key(comparator))[len(update) // 2]

        return part1, part2
