# Day 15 (2024)

`Warehouse Woes` ([prompt](https://adventofcode.com/2024/day/15))

One more 2D puzzle, today implementing some recursion and DFS.

## Part 1
In Part 1, the robot moves according to the input directions. The primary challenges involve handling obstacles, navigating open spaces, and managing special cases when moving boxes (`O`) to a valid position.

For the input handling we use our 2D grid and concatenate all the move instructions, as well as obtain the starting position for the robot, identified as `@`.
```py
class Solution(StrSplitSolution):
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
```
The robot can move in one of four directions: left (`<`), right (`>`), up (`^`), or down (`v`). Movement is handled by the `compute_move` function. This function processes each step and updates the robot’s position and the grid based on the following rules:
1. If the next cell is an obstacle (`#`): The robot doesn’t move.
2. If the next cell is empty (`.`): The robot moves into the cell, leaving its previous cell empty.
3. If the next cell contains a box (`O`): The robot pushes the box, and any other boxes present in that direction, forward until it encounters an obstacle or open space.
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
The robot processes the instructions iteratively. After executing all moves, the total score is computed based on the positions of the remaining boxes. Each one contributes `100 * row + column` to the score.
```py
class Solution(StrSplitSolution):
    def part_1(self) -> int:
        ...
        directions = {"<": (0, -1), ">": (0, 1), "^": (-1, 0), "v": (1, 0)}
        for move in moves:
            robot, grid = compute_move(robot, grid, directions[move])
        return sum(100 * pos[0] + pos[1] for pos in grid if grid[pos] == "O")

```
## Part 2
In Part 2, the input grid is transformed so that each box (`O`) is replaced with a wider representation `[]`. Similarly, the other grid elements are doubled horizontally to match the new dimensions of the boxes, except the robot (`@`). 
```py
class Solution(StrSplitSolution):
    def part_2(self) -> int:
        ...
        new_grid = ["" for _ in grid]
        for i in range(len(grid)):
            for elem in grid[i]:
                if elem == "@":
                    new_grid[i] += "@."
                elif elem == "O":
                    new_grid[i] += "[]"
                else:
                    new_grid[i] += elem * 2
```
With the new grid, the movement logic needs to account for the width of the boxes. A move involving the robot (`@`) now considers the following scenarios:

1. If the next cell is open space (`.`), the robot moves normally.
2. If the next cell is the right side of a box (`]`), both parts of the box (`[]`) must be moved in the specified direction.
3. If the next cell is the left side of a box (`[`), both parts of the box must be moved, ensuring no collisions with obstacles or other elements.  

The `vertical_move` function checks if a move in a given direction is valid, ensuring the wider box can be moved safely, through a recursive implementation fo DFS.

```py
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
```
The `execute_move` function updates the grid based on valid moves. It handles the wider box logic by recursively moving both parts of the box (`[]`) while ensuring grid consistency:
```py
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
```
The robot processes the movement instructions iteratively. Horizontal moves (`<` or `>`) use the same logic as in Part 1, while vertical moves (`^` or `v`) involve additional checks and handling for the wider boxes. Finally the score is computed using the position of the left side of the box (`[`).
```py
class Solution(StrSplitSolution):
    def part_2(self) -> int:
        ...
        directions = {"<": (0, -1), ">": (0, 1), "^": (-1, 0), "v": (1, 0)}
        for move in moves:
            if move in "<>":
                robot, grid = compute_move(robot, grid, directions[move])
            elif vertical_move(robot, grid, directions[move]):
                robot, grid = execute_move(robot, grid, directions[move])
        return sum(100 * pos[0] + pos[1] for pos in grid if grid[pos] == "[")
```
