# Generated using @xavdid's AoC Python Template: https://github.com/xavdid/advent-of-code-python-template

# puzzle prompt: https://adventofcode.com/2024/day/20

import heapq
from collections import defaultdict
from itertools import combinations

from ...base import StrSplitSolution, answer, slow

GridPoint = tuple[int, int]
Grid = dict[GridPoint, str]


def parse_grid(raw_grid: list[str]) -> Grid:
    """
    returns 2-tuples of (row, col) with their value
    """
    result = {}

    for row, line in enumerate(raw_grid):
        for col, c in enumerate(line):
            result[row, col] = c

    return result


def print_grid(grid: Grid):
    """
    Prints the grid in a pretty format
    """
    max_x = max(x for x, _ in grid)
    max_y = max(y for _, y in grid)
    for x in range(max_x + 1):
        for y in range(max_y + 1):
            print(grid.get((x, y), " "), end="")
        print()


def add_points(x: GridPoint, y: GridPoint) -> GridPoint:
    return (x[0] + y[0], x[1] + y[1])


def manhattan(x: GridPoint, y: GridPoint) -> int:
    return abs(x[0] - y[0]) + abs(x[1] - y[1])


def dijkstra(grid: Grid, start: GridPoint) -> dict:
    distances = defaultdict(lambda: (float("inf")))
    dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    distances[start] = 0
    queue = [(0, start)]
    while queue:
        dist, pos = heapq.heappop(queue)
        for ndi in dirs:
            npos, ndist = add_points(pos, ndi), dist + 1
            if grid[npos] != "#":
                o_dist = distances[npos]
                if o_dist >= ndist:
                    distances[npos] = ndist
                    heapq.heappush(queue, (ndist, npos))
    return dict(distances)


class Solution(StrSplitSolution):
    _year = 2024
    _day = 20

    # @answer(1234)
    def part_1(self) -> int:
        grid = parse_grid(self.input)
        start = list(grid.keys())[list(grid.values()).index("S")]
        distances = dijkstra(grid, start)
        result = 0
        for (p, i), (q, j) in combinations(distances.items(), 2):
            d = manhattan(p, q)
            if d == 2 and j - i - d >= 100:
                result += 1
        return result

    @slow
    @answer((1332, 987695))
    def solve(self) -> tuple[int, int]:
        grid = parse_grid(self.input)
        start = list(grid.keys())[list(grid.values()).index("S")]
        distances = dijkstra(grid, start)
        result1, result2 = 0, 0
        for (p, i), (q, j) in combinations(distances.items(), 2):
            d = manhattan(p, q)
            if d == 2 and j - i - d >= 100:
                result1 += 1
            if d < 21 and j - i - d >= 100:
                result2 += 1
        return result1, result2
