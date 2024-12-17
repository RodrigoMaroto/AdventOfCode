# Day 15 (2024)

`TITLE` ([prompt](https://adventofcode.com/2024/day/15))

Use this space for notes on the day's solution and to document what you've learned!

## Part 1

```py
def compute_move(robot: GridPoint, grid: Grid, direction: GridPoint) -> tuple[GridPoint, Grid]:
    next_pos = add_points(robot, direction)
    if grid[next_pos] == "#":
        pass
    if grid[next_pos] == ".":
        grid[robot], grid[next_pos] = ".", "@"
        robot = next_pos
    else:
        while grid[next_pos] == "O":
            next_pos = add_points(next_pos, direction)
        if grid[next_pos] == "#":
            return robot, grid
        grid[robot], grid[add_points(robot, direction)], grid[next_pos] = ".", "@", "O"
        robot = add_points(robot, direction)
    return robot, grid
```

## Part 2

