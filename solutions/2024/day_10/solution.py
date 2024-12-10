# Generated using @xavdid's AoC Python Template: https://github.com/xavdid/advent-of-code-python-template

# puzzle prompt: https://adventofcode.com/2024/day/10

from ...base import StrSplitSolution, answer

GridPoint = tuple[int, int]
Grid = dict[GridPoint, int]


def parse_grid(raw_grid: list[str]) -> Grid:
    """
    returns 2-tuples of (row, col) with their value
    """
    result = {}

    for row, line in enumerate(raw_grid):
        for col, c in enumerate(line):
            result[row, col] = int(c)

    return result


def get_neighbours(grid: Grid, location: GridPoint) -> tuple[GridPoint]:
    directions = ((1, 0), (-1, 0), (0, 1), (0, -1))
    return tuple(
        loc
        for v in directions
        if (loc := (location[0] + v[0], location[1] + v[1])) in grid
    )


def search(grid: Grid, location: GridPoint, prev_height: int) -> list[GridPoint]:
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
        grid = parse_grid(self.input)
        trailheads = [loc for loc in grid if grid[loc] == 0]
        reached_tops = [search(grid, start, -1) for start in trailheads]
        part1 = sum(len(set(x)) for x in reached_tops)
        part2 = sum(len(x) for x in reached_tops)
        return part1, part2
