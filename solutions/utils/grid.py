from typing import Literal, overload

type GridPoint = tuple[int, int]
type Grid = dict[GridPoint, str]
type IntGrid = dict[GridPoint, int]


@overload
def parse_grid(raw_grid: list[str]) -> Grid: ...
@overload
def parse_grid(raw_grid: list[str], *, ignore_chars: str) -> Grid: ...
@overload
def parse_grid(
    raw_grid: list[str], *, int_vals: Literal[True], ignore_chars: str = ""
) -> IntGrid: ...
@overload
def parse_grid(
    raw_grid: list[str], *, int_vals: Literal[False], ignore_chars: str = ""
) -> Grid: ...


def parse_grid(
    raw_grid: list[str], *, int_vals: bool = False, ignore_chars: str = ""
) -> Grid | IntGrid:
    """
    returns 2-tuples of (row, col) with their value. Values are `str` by default, but can be ints with `int_vals=True`.

    `ignore_chars` is for grid characters that aren't valid landing spots, like walls.

    ```
    (0, 0) ------> (0, 9)
      |              |
      |              |
      |              |
      |              |
      V              V
    (9, 0) ------> (9, 9)
    ```
    """
    result = {}
    ignore = set(ignore_chars)

    for row, line in enumerate(raw_grid):
        for col, c in enumerate(line):
            if c in ignore:
                continue

            val = int(c) if int_vals else c

            result[row, col] = val

    return result


def add_points(a: GridPoint, b: GridPoint) -> GridPoint:
    """
    add a pair of 2-tuples together. Useful for calculating a new position from a location and an offset
    """
    return a[0] + b[0], a[1] + b[1]


def manhattan_distance(x: GridPoint, y: GridPoint) -> int:
    return abs(x[0] - y[0]) + abs(x[1] - y[1])


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
