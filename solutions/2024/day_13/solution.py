# Generated using @xavdid's AoC Python Template: https://github.com/xavdid/advent-of-code-python-template

# puzzle prompt: https://adventofcode.com/2024/day/13

import re

from ...base import StrSplitSolution, answer


def cramer_solution(
    button_a: list[int], button_b: list[int], prize: list[int]
) -> tuple[int, int]:
    det = button_a[0] * button_b[1] - button_b[0] * button_a[1]
    x = (prize[0] * button_b[1] - button_b[0] * prize[1]) / det
    y = (button_a[0] * prize[1] - prize[0] * button_a[1]) / det
    if x % 1 == 0 and y % 1 == 0:
        return int(x), int(y)
    return 0, 0


class Solution(StrSplitSolution):
    _year = 2024
    _day = 13
    separator = "\n\n"

    @answer(28753)
    def part_1(self) -> int:
        data = [[int(i) for i in re.findall(r"\d+", s)] for s in self.input]
        result = 0
        for d in data:
            a, b = cramer_solution(d[0:2], d[2:4], d[4:])
            result += a * 3 + b
        return result

    @answer(102718967795500)
    def part_2(self) -> int:
        data = [[int(i) for i in re.findall(r"\d+", s)] for s in self.input]
        result = 0
        for d in data:
            a, b = cramer_solution(d[0:2], d[2:4], [10000000000000 + i for i in d[4:]])
            result += a * 3 + b
        return result

    @answer((28753, 102718967795500))
    def solve(self) -> tuple[int, int]:
        data = [[int(i) for i in re.findall(r"\d+", s)] for s in self.input]
        part1 = sum(
            a[0] * 3 + a[1]
            for d in data
            if (a := cramer_solution(d[0:2], d[2:4], d[4:]))
        )
        for line in data:
            line[-1] += 10000000000000
            line[-2] += 10000000000000
        part2 = sum(
            a[0] * 3 + a[1]
            for d in data
            if (a := cramer_solution(d[0:2], d[2:4], d[4:]))
        )
        return part1, part2
