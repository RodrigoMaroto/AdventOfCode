# Generated using @xavdid's AoC Python Template: https://github.com/xavdid/advent-of-code-python-template

# puzzle prompt: https://adventofcode.com/2024/day/19

from functools import cache

from ...base import StrSplitSolution, answer


@cache
def combs(patterns: tuple[str, ...], target: str) -> int:
    if not target:
        return 1
    return sum(
        combs(patterns, target[len(pat) :])
        for pat in patterns
        if target.startswith(pat)
    )


class Solution(StrSplitSolution):
    _year = 2024
    _day = 19

    @answer((374, 1100663950563322))
    def solve(self) -> tuple[int, int]:
        patterns, _, *designs = self.input
        patterns = tuple(x.strip() for x in patterns.split(","))
        combinations = [x for d in designs if (x := combs(patterns, d)) != 0]
        return len(combinations), sum(combinations)
