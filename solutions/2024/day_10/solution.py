# Generated using @xavdid's AoC Python Template: https://github.com/xavdid/advent-of-code-python-template

# puzzle prompt: https://adventofcode.com/2024/day/10

from ...base import StrSplitSolution, answer
from ...utils.grid import GridPoint, IntGrid, parse_grid


def get_neighbours(grid: IntGrid, location: GridPoint) -> tuple[GridPoint]:
    directions = ((1, 0), (-1, 0), (0, 1), (0, -1))
    return tuple(
        loc
        for v in directions
        if (loc := (location[0] + v[0], location[1] + v[1])) in grid
    )


def search(grid: IntGrid, location: GridPoint, prev_height: int) -> list[GridPoint]:
    height = grid[location]
    if height != prev_height + 1:
        return []
    if height == 9:
        return [location]
    locations = []
    for n in get_neighbours(grid, location):
        locations += search(grid, n, height)
    return locations


class Solution(StrSplitSolution):
    _year = 2024
    _day = 10

    @answer((744, 1651))
    def solve(self) -> tuple[int, int]:
        grid = parse_grid(self.input, int_vals=True)
        trailheads = [loc for loc in grid if grid[loc] == 0]
        reached_tops = [search(grid, start, -1) for start in trailheads]
        part1 = sum(len(set(x)) for x in reached_tops)
        part2 = sum(len(x) for x in reached_tops)
        return part1, part2
