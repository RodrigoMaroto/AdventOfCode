# Generated using @xavdid's AoC Python Template: https://github.com/xavdid/advent-of-code-python-template

# puzzle prompt: https://adventofcode.com/2024/day/15

from collections import deque

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


def compute_move(
    robot: GridPoint, grid: Grid, direction: GridPoint
) -> tuple[GridPoint, Grid]:
    next_pos = add_points(robot, direction)
    if grid[next_pos] == "#":
        pass
    if grid[next_pos] == ".":
        grid[robot], grid[next_pos] = ".", "@"
        robot = next_pos
    else:
        to_move = deque()
        to_move.append(robot)
        while grid[next_pos] in "O[]":
            to_move.append(next_pos)
            next_pos = add_points(next_pos, direction)
        if grid[next_pos] == "#":
            return robot, grid
        while to_move:
            move = to_move.pop()
            grid[add_points(move, direction)] = grid[move]
        grid[robot] = "."
        robot = add_points(robot, direction)
    return robot, grid


def vertical_move(pos: GridPoint, grid: Grid, direction: GridPoint) -> bool:
    next_pos = add_points(pos, direction)
    if grid[next_pos] == "#":
        return False
    if grid[next_pos] == ".":
        return True
    if grid[next_pos] == "[":
        checks = [add_points(next_pos, (0, 1)), next_pos]
        return all(vertical_move(p, grid, direction) for p in checks)
    if grid[next_pos] == "]":
        checks = [add_points(next_pos, (0, -1)), next_pos]
        return all(vertical_move(p, grid, direction) for p in checks)
    return False


def execute_move(
    pos: GridPoint, grid: Grid, direction: GridPoint
) -> tuple[GridPoint, Grid]:
    next_pos = add_points(pos, direction)
    curr_value = grid[pos]
    if grid[next_pos] == ".":
        grid[pos], grid[next_pos] = grid[next_pos], grid[pos]
    elif grid[next_pos] == "]":
        execute_move(next_pos, grid, direction)
        execute_move(add_points(next_pos, (0, -1)), grid, direction)
        grid[pos], grid[next_pos] = grid[next_pos], grid[pos]
    elif grid[next_pos] == "[":
        execute_move(next_pos, grid, direction)
        execute_move(add_points(next_pos, (0, 1)), grid, direction)
        grid[pos], grid[next_pos] = grid[next_pos], grid[pos]
    if curr_value == "@":
        pos = next_pos
    return pos, grid


class Solution(StrSplitSolution):
    _year = 2024
    _day = 15

    @answer(1514353)
    def part_1(self) -> int:
        grid, m = (
            self.input[: self.input.index("")],
            self.input[self.input.index("") + 1 :],
        )
        moves = ""
        for line in m:
            moves += line
        grid = parse_grid(grid)
        robot = list(grid.keys())[list(grid.values()).index("@")]
        directions = {"<": (0, -1), ">": (0, 1), "^": (-1, 0), "v": (1, 0)}
        for move in moves:
            robot, grid = compute_move(robot, grid, directions[move])
        return sum(100 * pos[0] + pos[1] for pos in grid if grid[pos] == "O")

    @answer(1533076)
    def part_2(self) -> int:
        grid, m = (
            self.input[: self.input.index("")],
            self.input[self.input.index("") + 1 :],
        )
        moves = ""
        for line in m:
            moves += line
        new_grid = ["" for _ in grid]
        for i in range(len(grid)):
            for elem in grid[i]:
                if elem == "@":
                    new_grid[i] += "@."
                elif elem == "O":
                    new_grid[i] += "[]"
                else:
                    new_grid[i] += elem * 2
        grid = parse_grid(new_grid)
        robot = list(grid.keys())[list(grid.values()).index("@")]
        directions = {"<": (0, -1), ">": (0, 1), "^": (-1, 0), "v": (1, 0)}
        for move in moves:
            if move in "<>":
                robot, grid = compute_move(robot, grid, directions[move])
            elif vertical_move(robot, grid, directions[move]):
                robot, grid = execute_move(robot, grid, directions[move])
        return sum(100 * pos[0] + pos[1] for pos in grid if grid[pos] == "[")
