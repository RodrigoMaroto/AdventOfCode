# Generated using @xavdid's AoC Python Template: https://github.com/xavdid/advent-of-code-python-template

# puzzle prompt: https://adventofcode.com/2024/day/20

import heapq
from collections import defaultdict
from itertools import combinations

from ...base import StrSplitSolution, answer, slow
from ...utils.grid import Grid, GridPoint, add_points, manhattan_distance, parse_grid


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
            d = manhattan_distance(p, q)
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
            d = manhattan_distance(p, q)
            if d == 2 and j - i - d >= 100:
                result1 += 1
            if d < 21 and j - i - d >= 100:
                result2 += 1
        return result1, result2
