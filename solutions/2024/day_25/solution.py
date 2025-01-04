# Generated using @xavdid's AoC Python Template: https://github.com/xavdid/advent-of-code-python-template

# puzzle prompt: https://adventofcode.com/2024/day/25

from ...base import TextSolution, answer


def parse_heights(grid: str) -> tuple[int, ...]:
    return tuple(col.count("#") - 1 for col in zip(*grid.split("\n")))


def fits(key: tuple[int, ...], lock: tuple[int, ...]) -> bool:
    return all((l + k <= 5 for l, k in zip(lock, key)))


class Solution(TextSolution):
    _year = 2024
    _day = 25

    @answer(3307)
    def part_1(self) -> int:
        grids = self.input.split("\n\n")

        locks, keys = [], []
        for i in grids:
            if i[0] == "#":
                locks.append(parse_heights(i))
            else:
                keys.append(parse_heights(i))
        return sum(fits(key, lock) for lock in locks for key in keys)
