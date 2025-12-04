# Generated using @xavdid's AoC Python Template: https://github.com/xavdid/advent-of-code-python-template

# puzzle prompt: https://adventofcode.com/2025/day/4

from ...base import StrSplitSolution, answer
from ...utils.grid import Grid, GridPoint, parse_grid, adjacent_points


class Solution(StrSplitSolution):
    _year = 2025
    _day = 4

    @answer(1480)
    def part_1(self) -> int:
        result = 0
        grid: Grid = parse_grid(self.input)
        for point in grid:
            if grid[point] == "@":
                neighbors = [grid[n] for n in adjacent_points(point, grid=grid) if grid[n] == "@"]
                result += 1 if len(neighbors) < 4 else 0
        return result

    def remove_rolls(self, grid: Grid) -> int:
        result = 0
        to_remove = set()
        for point in grid:
            if grid[point] == "@":
                neighbors = [n for n in adjacent_points(point, grid=grid) if grid[n] == "@"]
                if len(neighbors) < 4:
                    to_remove.add(point)
        for point in to_remove:
            grid[point] = "."
            result += 1
        return result


    # @answer(1234)
    def part_2(self) -> int:
        result = 0
        rolls_removed = -1
        grid: Grid = parse_grid(self.input)
        while rolls_removed != 0:
            rolls_removed = self.remove_rolls(grid)
            result += rolls_removed
        return result

    @answer((1480, 8899))
    def solve(self) -> tuple[int, int]:
        result1, result2 = 0, 0
        grid: Grid = parse_grid(self.input)
        result1 = self.remove_rolls(grid)
        rolls_removed, result2 = result1, result1
        while rolls_removed != 0:
            rolls_removed = self.remove_rolls(grid)
            result2 += rolls_removed
        return result1, result2

