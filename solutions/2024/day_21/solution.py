# Generated using @xavdid's AoC Python Template: https://github.com/xavdid/advent-of-code-python-template

# puzzle prompt: https://adventofcode.com/2024/day/21

from functools import cache

from ...base import StrSplitSolution, answer

num_pad = {
    "7": (0, 0),
    "8": (0, 1),
    "9": (0, 2),
    "4": (1, 0),
    "5": (1, 1),
    "6": (1, 2),
    "1": (2, 0),
    "2": (2, 1),
    "3": (2, 2),
    " ": (3, 0),
    "0": (3, 1),
    "A": (3, 2),
}

dir_pad = {
    " ": (0, 0),
    "^": (0, 1),
    "A": (0, 2),
    "<": (1, 0),
    "v": (1, 1),
    ">": (1, 2),
}


def shortestPath(key1: str, key2: str, isNumPad: bool) -> str:
    pad = num_pad if isNumPad else dir_pad
    r1, c1 = pad[key1]
    r2, c2 = pad[key2]

    ud = "v" * (r2 - r1) if r2 > r1 else "^" * (r1 - r2)
    lr = ">" * (c2 - c1) if c2 > c1 else "<" * (c1 - c2)

    if c2 > c1 and (r2, c1) != pad[" "]:
        # Safe to move vertically first if heading right and corner point isn't the gap
        return ud + lr + "A"

    if (r1, c2) != pad[" "]:
        # Safe to move horizontally first if corner point isn't the gap
        return lr + ud + "A"
    # Must be safe to move vertically first because we can't be in same column as gap.
    return ud + lr + "A"


@cache
def solve(s: str, l: int, d: int) -> int:
    if l > d:
        return len(s)
    return sum(solve(shortestPath(f, t, not l), l + 1, d) for f, t in zip("A" + s, s))


class Solution(StrSplitSolution):
    _year = 2024
    _day = 21

    @answer(182844)
    def part_1(self) -> int:
        return sum(solve(code, 0, 2) * int(code[:-1]) for code in self.input)

    @answer(226179529377982)
    def part_2(self) -> int:
        return sum(solve(code, 0, 25) * int(code[:-1]) for code in self.input)
