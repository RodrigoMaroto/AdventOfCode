# Generated using @xavdid's AoC Python Template: https://github.com/xavdid/advent-of-code-python-template

# puzzle prompt: https://adventofcode.com/2024/day/6

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


def update_direction(direction: tuple[int, int]) -> tuple[int, int]:
    if direction[1] == 0:
        return (0, -direction[0])
    return (direction[1], 0)


def track_guard(grid: Grid) -> tuple[bool, set]:
    guard_pos = list(grid.keys())[list(grid.values()).index("^")]
    guard_direction = (-1, 0)
    visited = set()

    while True:
        visited.add((guard_pos, guard_direction))
        new_pos = (guard_pos[0] + guard_direction[0], guard_pos[1] + guard_direction[1])

        if new_pos not in grid:
            break

        if grid[new_pos] == "#":
            guard_direction = update_direction(guard_direction)
            visited.add((guard_pos, guard_direction))

        else:
            to_add = new_pos, guard_direction
            if to_add in visited:
                # loop!
                return False, set()

            visited.add(to_add)
            guard_pos = new_pos

    return True, {l for l, _ in visited}


def track_guard_old(grid: Grid) -> tuple[bool, set]:
    guard_pos = list(grid.keys())[list(grid.values()).index("^")]
    guard_direction = (-1, 0)
    visited = set()

    while True:
        visited.add((guard_pos, guard_direction))
        new_pos = (guard_pos[0] + guard_direction[0], guard_pos[1] + guard_direction[1])

        if new_pos not in grid:
            break

        if grid[new_pos] == "#":
            guard_direction = update_direction(guard_direction)
            visited.add((guard_pos, guard_direction))

        else:
            to_add = new_pos, guard_direction
            if to_add in visited:
                # loop!
                return False, set()

            visited.add(to_add)
            guard_pos = new_pos

    return True, {l for l, _ in visited}


class Solution(StrSplitSolution):
    _year = 2024
    _day = 6

    @answer(4515)
    def part_1(self) -> int:
        grid = parse_grid(self.input)
        return len(track_guard(grid)[1])

    @slow
    @answer(1309)
    def part_2(self) -> int:
        grid = parse_grid(self.input)
        _, path = track_guard(grid)
        result = 0
        for pos in path:
            if grid[pos] == "^":
                continue
            grid[pos] = "#"
            if not track_guard(grid)[0]:
                result += 1
            grid[pos] = "."

        return result
