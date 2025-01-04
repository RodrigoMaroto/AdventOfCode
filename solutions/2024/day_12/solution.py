# Generated using @xavdid's AoC Python Template: https://github.com/xavdid/advent-of-code-python-template

# puzzle prompt: https://adventofcode.com/2024/day/12

from ...base import StrSplitSolution, answer
from ...utils.grid import Grid, GridPoint, add_points, parse_grid

visited = set()


def plotRegion(
    region: set[GridPoint], grid: Grid, location: GridPoint
) -> set[GridPoint]:
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    region.add(location)
    visited.add(location)
    for d in directions:
        new_loc = add_points(location, d)
        if (
            new_loc in grid
            and grid[location] == grid[new_loc]
            and new_loc not in region
        ):
            plotRegion(region, grid, new_loc)
    return region


def perimeter(region: set[GridPoint]) -> int:
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    return sum(
        [1 for plot in region for d in directions if add_points(plot, d) not in region]
    )


def sides(region: set[GridPoint]) -> int:
    out_corners = [
        [(-1, 0), (0, -1)],
        [(-1, 0), (0, 1)],
        [(1, 0), (0, -1)],
        [(1, 0), (0, 1)],
    ]
    res = 0
    for plot in region:
        for c in out_corners:
            if all(add_points(plot, d) not in region for d in c) or (
                all(add_points(plot, d) in region for d in c)
                and add_points(plot, add_points(c[0], c[1])) not in region
            ):
                res += 1
    return res


class Solution(StrSplitSolution):
    _year = 2024
    _day = 12

    @answer(1452678)
    def part_1(self) -> int:
        grid = parse_grid(self.input)
        regions = [plotRegion(set(), grid, pos) for pos in grid if pos not in visited]
        return sum(len(r) * perimeter(r) for r in regions)

    @answer((1452678, 873584))
    def solve(self) -> tuple[int, int]:
        grid = parse_grid(self.input)
        regions = [plotRegion(set(), grid, pos) for pos in grid if pos not in visited]
        part1 = sum(len(r) * perimeter(r) for r in regions)
        part2 = sum(len(r) * sides(r) for r in regions)
        return part1, part2
