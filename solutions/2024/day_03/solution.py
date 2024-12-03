# Generated using @xavdid's AoC Python Template: https://github.com/xavdid/advent-of-code-python-template

# puzzle prompt: https://adventofcode.com/2024/day/3

import re

from ...base import TextSolution, answer


class Solution(TextSolution):
    _year = 2024
    _day = 3

    @answer(180233229)
    def part_1(self) -> int:
        valid_expr = re.findall(r"mul\((\d{1,3}),(\d{1,3})\)", self.input)
        return sum(int(x[0]) * int(x[1]) for x in valid_expr)

    @answer(95411583)
    def part_2(self) -> int:
        valid_code = self.input.split("do()")
        valid_code = [x.split("don't()")[0] for x in valid_code]
        valid_code = "".join(valid_code)
        valid_expr = re.findall(r"mul\((\d{1,3}),(\d{1,3})\)", valid_code)
        return sum(int(x[0]) * int(x[1]) for x in valid_expr)
