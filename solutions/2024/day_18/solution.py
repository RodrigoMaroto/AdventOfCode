# Generated using @xavdid's AoC Python Template: https://github.com/xavdid/advent-of-code-python-template

# puzzle prompt: https://adventofcode.com/2024/day/18

from ...base import StrSplitSolution, answer

GridPoint = tuple[int, int]
Grid = dict[GridPoint, str]


def parse_grid() -> Grid:
    """
    returns 2-tuples of (row, col) with their value
    """
    result = {}

    for row in range(71):
        for col in range(71):
            result[row, col] = "."

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


def run(iterations: int, obstacles: list[str]) -> int:
    grid = parse_grid()
    for i in range(iterations):
        point = GridPoint(map(int, obstacles[i].split(",")))
        grid[point] = "#"
    return dijkstra(grid, (0, 0), (70, 70))


class Solution(StrSplitSolution):
    _year = 2024
    _day = 18

    @answer(330)
    def part_1(self) -> int:
        return run(1024, self.input)

    @answer("10,38")
    def part_2(self) -> str:
        low = 0
        high = len(self.input)
        while high - low > 1:
            avg = (low + high) // 2
            if run(avg, self.input) == -1:
                high = avg
            else:
                low = avg
        return self.input[low]
