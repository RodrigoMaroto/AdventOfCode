# Generated using @xavdid's AoC Python Template: https://github.com/xavdid/advent-of-code-python-template

# puzzle prompt: https://adventofcode.com/2024/day/18

from ...base import StrSplitSolution, answer
from ...utils.grid import Grid, GridPoint, add_points


def parse_grid(size: int) -> Grid:
    result = {}

    for row in range(size):
        for col in range(size):
            result[row, col] = "."

    return result


def dijkstra(grid: Grid, start: GridPoint, end: GridPoint) -> int:
    dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    open_set = [(0, start)]
    closed_set = {start}

    while open_set:
        score, target = open_set.pop(0)

        if target == end:
            return score

        for d in dirs:
            ntarget = add_points(target, d)
            if ntarget not in closed_set and ntarget in grid and grid[ntarget] != "#":
                open_set.append((score + 1, ntarget))
                closed_set.add(ntarget)
    return -1


def run(iterations: int, obstacles: list[str], size: int) -> int:
    grid = parse_grid(size)
    for i in range(iterations):
        point = tuple(map(int, obstacles[i].split(",")))
        grid[(point[0], point[1])] = "#"
    return dijkstra(grid, (0, 0), (size - 1, size - 1))


class Solution(StrSplitSolution):
    _year = 2024
    _day = 18

    @answer(330)
    def part_1(self) -> int:
        if self.use_test_data:
            return run(12, self.input, 7)
        return run(1024, self.input, 71)

    @answer("10,38")
    def part_2(self) -> str:
        size = 7 if self.use_test_data else 71
        low = 0
        high = len(self.input)
        while high - low > 1:
            avg = (low + high) // 2
            if run(avg, self.input, size) == -1:
                high = avg
            else:
                low = avg
        return self.input[low]
