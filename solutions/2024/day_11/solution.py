# Generated using @xavdid's AoC Python Template: https://github.com/xavdid/advent-of-code-python-template

# puzzle prompt: https://adventofcode.com/2024/day/11

from functools import cache

from ...base import IntSplitSolution, answer


def update_stones(stones: list[int]) -> list[int]:
    result = []
    for stone in stones:
        if stone == 0:
            result.append(1)
        elif (length := len(str(stone))) % 2 == 0:
            result.append(int(str(stone)[: length // 2]))
            result.append(int(str(stone)[length // 2 :]))
        else:
            result.append(stone * 2024)
    return result


@cache
def solve(stone: int, blinks: int) -> int:
    if blinks == 0:
        return 1
    if stone == 0:
        return solve(1, blinks - 1)
    if len(str_stone := str(stone)) % 2 == 0:
        mid = len(str_stone) // 2
        return solve(int(str_stone[:mid]), blinks - 1) + solve(
            int(str_stone[mid:]), blinks - 1
        )
    return solve(stone * 2024, blinks - 1)


class Solution(IntSplitSolution):
    _year = 2024
    _day = 11
    separator = " "

    @answer(198075)
    def part_1(self) -> int:
        stones = self.input.copy()
        for _ in range(25):
            stones = update_stones(stones)
        return len(stones)

    @answer(235571309320764)
    def part_2(self) -> int:
        return sum(solve(stone, 75) for stone in self.input)

    @answer((198075, 235571309320764))
    def solve(self) -> tuple[int, int]:
        return sum(solve(stone, 25) for stone in self.input), sum(
            solve(stone, 75) for stone in self.input
        )
