# Generated using @xavdid's AoC Python Template: https://github.com/xavdid/advent-of-code-python-template

# puzzle prompt: https://adventofcode.com/2024/day/16

import heapq
from collections import defaultdict

from ...base import StrSplitSolution, answer

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


def seg(x: GridPoint, y: GridPoint) -> tuple[int, ...]:
    return tuple(v for t in sorted([x, y]) for v in t)


def countsegs(segset: set) -> int:
    ret, points = 0, set()
    for a, b, c, d in segset:
        ret += abs(a - c) + abs(b - d) + 1 - ((a, b) in points) - ((c, d) in points)
        points.update({(a, b), (c, d)})
    return ret


def dijkstra(grid: Grid, start: GridPoint, end: GridPoint) -> tuple[int, int]:
    distances = defaultdict(lambda: (float("inf"), set()))
    dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    distances[start, 1] = (0, set())
    queue = [(0, start, 1)]
    while queue:
        dist, pos, di = heapq.heappop(queue)
        _, p_set = distances[pos, di]
        for ndi in range(-1, 2):
            ndir = dirs[(di + ndi) % 4]
            npos, ndist = add_points(pos, ndir), dist + 1 + 1000 * (ndi != 0)
            while (
                grid[npos] != "#"
                and grid[(npos[0] + ndir[1], npos[1] + ndir[0])] == "#"
                and grid[(npos[0] - ndir[1], npos[1] - ndir[0])] == "#"
            ):
                npos, ndist = add_points(npos, ndir), ndist + 1
            nset = p_set | {seg(pos, npos)}
            if npos == end:
                return ndist, countsegs(nset)
            if grid[npos] != "#":
                o_dist, o_set = distances[npos, (di + ndi) % 4]
                if o_dist == ndist and any((pos not in o_set) for pos in nset):
                    o_set.update(nset)
                    heapq.heappush(queue, (ndist, npos, (di + ndi) % 4))
                if o_dist > ndist:
                    distances[npos, (di + ndi) % 4] = ndist, nset
                    heapq.heappush(queue, (ndist, npos, (di + ndi) % 4))
    return 0, 0


class Solution(StrSplitSolution):
    _year = 2024
    _day = 16

    @answer((133584, 622))
    def solve(self) -> tuple[int, int]:
        grid = parse_grid(self.input)
        start = list(grid.keys())[list(grid.values()).index("S")]
        end = list(grid.keys())[list(grid.values()).index("E")]
        return dijkstra(grid, start, end)
